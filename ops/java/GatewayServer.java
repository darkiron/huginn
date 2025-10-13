import com.sun.net.httpserver.HttpExchange;
import com.sun.net.httpserver.HttpHandler;
import com.sun.net.httpserver.HttpServer;

import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.net.HttpURLConnection;
import java.net.InetSocketAddress;
import java.net.URL;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.List;
import java.util.Map;

public class GatewayServer {

    public static void main(String[] args) throws IOException {
        HttpServer server = HttpServer.create(new InetSocketAddress(8080), 0);
        server.createContext("/", new HtmlHandler());
        System.out.println("🚀 Java Gateway running on http://localhost:8080");
        server.start();
    }

    static class HtmlHandler implements HttpHandler {

        @Override
        public void handle(HttpExchange exchange) throws IOException {
            long t0 = System.currentTimeMillis();
            String path = exchange.getRequestURI().getPath();

            int status;
            byte[] bodyBytes = null;
            String html = null;
            Map<String, List<String>> proxiedHeaders = null;

            if (path.startsWith("/php")) {
                // Strip le prefix /php (ex: /php -> /)
                String stripped = path.equals("/php") ? "/" : path.substring(4);
                ProxyResp pr = forwardToLaravel(exchange, stripped);
                status = pr.code;
                proxiedHeaders = pr.headers;
                String ct = firstHeader(proxiedHeaders, "Content-Type");
                boolean isHtml = ct != null && ct.toLowerCase().contains("text/html");
                if (isHtml) {
                    html = new String(pr.body, StandardCharsets.UTF_8);
                } else {
                    bodyBytes = pr.body;
                }
            } else {
                // Statique: / -> index.html ; sinon sert fichiers sous /app/ui/web
                Path root = Path.of("ui/web");
                Path file = path.equals("/") ? root.resolve("index.html") : root.resolve(path.substring(1)).normalize();

                if (!file.startsWith(root) || !Files.exists(file) || Files.isDirectory(file)) {
                    // 404 simple
                    String notFound = "<h1>404</h1>";
                    exchange.getResponseHeaders().set("Content-Type", "text/html; charset=UTF-8");
                    exchange.sendResponseHeaders(404, notFound.getBytes(StandardCharsets.UTF_8).length);
                    try (OutputStream os = exchange.getResponseBody()) { os.write(notFound.getBytes(StandardCharsets.UTF_8)); }
                    return;
                }

                byte[] content = Files.readAllBytes(file);
                String ct = guessContentType(file);
                exchange.getResponseHeaders().set("Content-Type", ct);
                exchange.sendResponseHeaders(200, content.length);
                try (OutputStream os = exchange.getResponseBody()) { os.write(content); }
                return;
            }

            long latency = System.currentTimeMillis() - t0;
            long usedBytes = Runtime.getRuntime().totalMemory() - Runtime.getRuntime().freeMemory();
            long memory = usedBytes / (1024 * 1024);

            if (html != null) {
                String container = Files.readString(Path.of("ui/web/widget-container.html"), StandardCharsets.UTF_8);
                String script = Files.readString(Path.of("ui/web/widget-script.html"), StandardCharsets.UTF_8)
                        .replace("{{latency}}", String.valueOf(latency))
                        .replace("{{memory}}", String.valueOf(memory));

                String finalHtml = injectBeforeBodyEnd(html, container + script);
                byte[] out = finalHtml.getBytes(StandardCharsets.UTF_8);

                if (proxiedHeaders != null) {
                    for (Map.Entry<String, List<String>> e : proxiedHeaders.entrySet()) {
                        String key = e.getKey();
                        if (key == null) continue;
                        if (key.equalsIgnoreCase("Content-Length") || key.equalsIgnoreCase("Content-Type")) continue;
                        exchange.getResponseHeaders().put(key, e.getValue());
                    }
                }
                exchange.getResponseHeaders().set("Content-Type", "text/html; charset=UTF-8");
                exchange.sendResponseHeaders(status, out.length);
                try (OutputStream os = exchange.getResponseBody()) { os.write(out); }
            } else {
                if (proxiedHeaders != null) {
                    for (Map.Entry<String, List<String>> e : proxiedHeaders.entrySet()) {
                        String key = e.getKey();
                        if (key == null) continue;
                        if (key.equalsIgnoreCase("Content-Length")) continue;
                        exchange.getResponseHeaders().put(key, e.getValue());
                    }
                }
                if (bodyBytes == null) bodyBytes = new byte[0];
                exchange.sendResponseHeaders(status, bodyBytes.length);
                try (OutputStream os = exchange.getResponseBody()) { os.write(bodyBytes); }
            }
        }

        static class ProxyResp {
            int code; byte[] body; Map<String, List<String>> headers;
            ProxyResp(int code, byte[] body, Map<String, List<String>> headers) {
                this.code = code; this.body = body; this.headers = headers;
            }
        }

        private ProxyResp forwardToLaravel(HttpExchange exchange, String targetPath) throws IOException {
            // IMPORTANT: cible = service docker 'laravel-front' port container 8080
            String rawQuery = exchange.getRequestURI().getRawQuery();
            String target = "http://laravel-front:8080" + targetPath + (rawQuery != null ? ("?" + rawQuery) : "");

            HttpURLConnection conn = (HttpURLConnection) new URL(target).openConnection();
            conn.setInstanceFollowRedirects(false);
            conn.setRequestMethod(exchange.getRequestMethod());

            for (Map.Entry<String, List<String>> h : exchange.getRequestHeaders().entrySet()) {
                String key = h.getKey();
                if (key == null) continue;
                if (key.equalsIgnoreCase("Host") || key.equalsIgnoreCase("Content-Length")) continue;
                for (String v : h.getValue()) conn.addRequestProperty(key, v);
            }

            String method = exchange.getRequestMethod();
            if (method.equalsIgnoreCase("POST") || method.equalsIgnoreCase("PUT")
                    || method.equalsIgnoreCase("PATCH") || method.equalsIgnoreCase("DELETE")) {
                conn.setDoOutput(true);
                try (InputStream req = exchange.getRequestBody(); OutputStream os = conn.getOutputStream()) {
                    req.transferTo(os);
                }
            }

            int code = conn.getResponseCode();
            Map<String, List<String>> headers = conn.getHeaderFields();
            InputStream rs = code >= 400 ? conn.getErrorStream() : conn.getInputStream();
            byte[] body = rs != null ? rs.readAllBytes() : new byte[0];
            conn.disconnect();
            return new ProxyResp(code, body, headers);
        }

        private static String firstHeader(Map<String, List<String>> headers, String name) {
            if (headers == null) return null;
            for (Map.Entry<String, List<String>> e : headers.entrySet()) {
                if (e.getKey() != null && e.getKey().equalsIgnoreCase(name)) {
                    List<String> vals = e.getValue();
                    if (vals != null && !vals.isEmpty()) return vals.get(0);
                }
            }
            return null;
        }

        private static String injectBeforeBodyEnd(String html, String widget) {
            return html.contains("</body>") ? html.replace("</body>", widget + "</body>") : html + widget;
        }

        private static String guessContentType(Path file) {
            String name = file.getFileName().toString().toLowerCase();
            if (name.endsWith(".html") || name.endsWith(".htm")) return "text/html; charset=UTF-8";
            if (name.endsWith(".css")) return "text/css; charset=UTF-8";
            if (name.endsWith(".js")) return "application/javascript; charset=UTF-8";
            if (name.endsWith(".svg")) return "image/svg+xml";
            if (name.endsWith(".png")) return "image/png";
            if (name.endsWith(".jpg") || name.endsWith(".jpeg")) return "image/jpeg";
            if (name.endsWith(".json")) return "application/json; charset=UTF-8";
            return "application/octet-stream";
        }
    }
}

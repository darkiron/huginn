// GatewayServer.java
// Minimal HTTP gateway (JDK HttpServer) : proxy vers PHP et injection widget.
// Compile avec: javac GatewayServer.java
// Run: java GatewayServer

import com.sun.net.httpserver.HttpExchange;
import com.sun.net.httpserver.HttpHandler;
import com.sun.net.httpserver.HttpServer;

import java.io.ByteArrayOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.net.HttpURLConnection;
import java.net.InetSocketAddress;
import java.net.URL;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;

public class GatewayServer {

    public static void main(String[] args) throws IOException {
        // Démarre le serveur HTTP sur le port 8080
        HttpServer server = HttpServer.create(new InetSocketAddress(8080), 0);
        server.createContext("/", new HtmlHandler());
        System.out.println("🚀 Java Gateway running on http://localhost:8080");
        server.start();
    }

    /**
     * HtmlHandler:
     * - si l'URL commence par /php -> proxy GET vers php-gateway:9000
     * - sinon -> sert ui/web/index.html
     * - dans tous les cas -> injecte ui/web/widget.html (avec placeholders remplacés)
     *
     * Ce handler lit totalement les flux distants et déconnecte proprement.
     */
    static class HtmlHandler implements HttpHandler {

        @Override
        public void handle(HttpExchange exchange) throws IOException {
            long t0 = System.currentTimeMillis();

            String path = exchange.getRequestURI().getPath();
            String response;

            if (path.startsWith("/php")) {
                response = proxyPhp(path);
            } else {
                // sert ui/web/index.html
                response = Files.readString(Path.of("ui/web/index.html"), StandardCharsets.UTF_8);
            }

            // calcul métriques
            long latency = System.currentTimeMillis() - t0;
            long usedBytes = Runtime.getRuntime().totalMemory() - Runtime.getRuntime().freeMemory();
            long memory = usedBytes / (1024 * 1024);

            // charger widget-container + widget-script
            String container = Files.readString(Path.of("ui/web/widget-container.html"), StandardCharsets.UTF_8);
            String script = Files.readString(Path.of("ui/web/widget-script.html"), StandardCharsets.UTF_8)
                    .replace("{{latency}}", String.valueOf(latency))
                    .replace("{{memory}}", String.valueOf(memory));

            String widget = container + script;

            // injecter avant </body>
            String finalHtml = response.contains("</body>")
                    ? response.replace("</body>", widget + "</body>")
                    : response + widget;

            // envoyer
            byte[] body = finalHtml.getBytes(StandardCharsets.UTF_8);
            exchange.getResponseHeaders().add("Content-Type", "text/html; charset=UTF-8");
            exchange.sendResponseHeaders(200, body.length);
            try (OutputStream os = exchange.getResponseBody()) {
                os.write(body);
            }
        }

        private String proxyPhp(String path) throws IOException {
            URL url = new URL("http://php-gateway:9000" + path);
            HttpURLConnection conn = (HttpURLConnection) url.openConnection();
            conn.setRequestMethod("GET");
            conn.setRequestProperty("Connection", "close");

            try (InputStream is = conn.getInputStream()) {
                return new String(is.readAllBytes(), StandardCharsets.UTF_8);
            } finally {
                conn.disconnect();
            }
        }
    }

}

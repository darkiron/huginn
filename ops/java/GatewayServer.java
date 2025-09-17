// On importe les classes nécessaires pour créer un serveur HTTP basique
import com.sun.net.httpserver.HttpServer;
import com.sun.net.httpserver.HttpHandler;
import com.sun.net.httpserver.HttpExchange;

import java.io.IOException;       // Gérer les erreurs d'entrée/sortie
import java.io.OutputStream;     // Écrire la réponse HTTP
import java.net.InetSocketAddress; // Définir l’adresse/port du serveur
import java.nio.file.Files;      // Lire les fichiers du disque
import java.nio.file.Path;       // Représenter un chemin vers un fichier

public class GatewayServer {
    public static void main(String[] args) throws IOException {
        // On démarre un serveur HTTP qui écoute sur le port 8080
        HttpServer server = HttpServer.create(new InetSocketAddress(8080), 0);

        // Toutes les routes "/" seront gérées par notre classe HtmlHandler
        server.createContext("/", new HtmlHandler());

        // Message dans la console pour confirmer que le serveur tourne
        System.out.println("🚀 Java Gateway running on http://localhost:8080");

        // On démarre le serveur (boucle infinie tant qu’on ne l’arrête pas)
        server.start();
    }

   // Une classe interne statique qui implémente une interface de Java.
   // Ici, HttpHandler est une INTERFACE : ça veut dire qu’elle définit un contrat (méthode handle à implémenter).
   static class HtmlHandler implements HttpHandler {

       // @Override est une ANNOTATION.
       // Elle dit au compilateur : "cette méthode redéfinit une méthode de l’interface ou d’une classe parente".
       // Si tu te trompes dans la signature (ex: mauvais nom ou mauvais type), le compilateur lèvera une erreur.
       @Override
       public void handle(HttpExchange exchange) throws IOException {
           // HttpExchange est une CLASSE fournie par com.sun.net.httpserver.
           // Elle encapsule TOUT ce qui concerne une requête HTTP :
           //   - les headers reçus
           //   - le body de la requête (si POST/PUT)
           //   - les infos de la réponse (headers, code HTTP, body à écrire)

           // Exemple : ici on mesure le temps pour calculer la latence.
           long startTime = System.currentTimeMillis();

           // Path et Files sont des CLASSES utilitaires de java.nio.file
           // Path = représente un chemin vers un fichier
           // Files = classe utilitaire avec des méthodes statiques pour lire/écrire
           Path indexPath = Path.of("ui/web/index.html");
           String baseHtml = Files.readString(indexPath);

           // Runtime est une CLASSE spéciale en Java :
           // - Elle représente la JVM en cours d’exécution
           // - On y accède par Singleton : Runtime.getRuntime()
           // Ici on s’en sert pour interroger la mémoire :
           long latencyMs = System.currentTimeMillis() - startTime;
           long totalMemory = Runtime.getRuntime().totalMemory();
           long freeMemory = Runtime.getRuntime().freeMemory();
           long usedMemory = totalMemory - freeMemory;

           // On convertit en MB (en Java, les divisions d'entiers tronquent les décimales → attention à ça).
           long usedMemoryMB = usedMemory / (1024 * 1024);

            // Charger les deux fichiers séparés
            String widgetContainer = Files.readString(Path.of("ui/web/widget-container.html"));
            String widgetScript = Files.readString(Path.of("ui/web/widget-script.html"));

            // Injecter le conteneur (dans le body)
            baseHtml = baseHtml.replace("</body>", widgetContainer + "</body>");

            // Puis injecter le script (juste avant </html>)
            widgetScript = widgetScript.replace("{{latency}}", String.valueOf(latencyMs))
                                       .replace("{{memory}}", String.valueOf(usedMemoryMB));

            String finalHtml = baseHtml.replace("</html>", widgetScript + "</html>");

           // exchange.getResponseHeaders() → permet de modifier les HEADERS HTTP envoyés au client.
           // Ici on précise que c’est du HTML avec encodage UTF-8.
           exchange.getResponseHeaders().add("Content-Type", "text/html; charset=UTF-8");

           // exchange.sendResponseHeaders(statusCode, length) → envoie le code HTTP (200 = OK)
           // et la taille du contenu qu’on va écrire.
           exchange.sendResponseHeaders(200, finalHtml.getBytes().length);


           // OutputStream = flux de sortie pour écrire la réponse au client.
           try (OutputStream os = exchange.getResponseBody()) {
               os.write(finalHtml.getBytes());
           }
           // Ici on utilise try-with-resources → ça ferme automatiquement le flux à la fin.
           // C’est un mécanisme introduit en Java 7 basé sur l’interface AutoCloseable.
       }
   }

}

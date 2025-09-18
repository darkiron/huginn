FROM openjdk:17-jdk-slim

WORKDIR /app

# Copier uniquement le serveur Java (on ne copie pas le widget si on monte en volume)
COPY ops/java/GatewayServer.java /app/

RUN javac GatewayServer.java

CMD ["java", "GatewayServer"]

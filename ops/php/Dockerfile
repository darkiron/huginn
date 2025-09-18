# On utilise l’image officielle PHP 8.3 (version CLI pour commencer)
FROM php:8.3-cli

# Définir le répertoire de travail dans le conteneur
WORKDIR /app

# Copier le code source PHP
COPY ../../apps/php/public/ /app/public

# Exposer le port interne 9000
EXPOSE 9000

# Lancer le serveur intégré de PHP
CMD ["php", "-S", "0.0.0.0:9000", "-t", "public"]

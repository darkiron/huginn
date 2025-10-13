FROM php:8.3-cli

# Install required system packages and PHP extensions
RUN apt-get update && apt-get install -y git unzip libzip-dev \
    && docker-php-ext-install zip pdo_mysql

# Composer (available in the image for runtime operations)
COPY --from=composer:2 /usr/bin/composer /usr/bin/composer

# Set working directory for the Laravel app (will be mounted at runtime)
WORKDIR /var/www/html

# Note: The application code is mounted via docker-compose at runtime:
#   volumes:
#     - ./apps/laravel-front:/var/www/html
# Therefore we do not copy source code or run composer install at build time.

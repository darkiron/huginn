# syntax=docker/dockerfile:1

# Base image with PHP and Composer
FROM php:8.3-cli AS base

# --- System and PHP dependencies + Composer ---
RUN apt-get update && apt-get install -y \
    git \
    unzip \
    zip \
    libicu-dev \
    libzip-dev \
    && docker-php-ext-install intl zip opcache \
    && curl -sS https://getcomposer.org/installer | php -- --install-dir=/usr/local/bin --filename=composer

# Builder stage: prepare app (either existing project or create new)
FROM base AS builder
WORKDIR /src

# Copy the Symfony app folder from the monorepo into the image (works even if empty)
# This path must match the docker-compose volume/path for the Symfony app
ARG APP_PATH=apps/symfony-back
COPY ${APP_PATH}/ ./

# Install dependencies if composer.json exists, otherwise create a new Symfony project
RUN if [ -f "composer.json" ]; then \
        echo "📦 Installing Symfony dependencies..." && \
        composer install --no-dev --optimize-autoloader --no-interaction; \
    else \
        echo "✨ Creating new Symfony project..." && \
        composer create-project symfony/skeleton . --no-interaction && \
        composer require symfony/http-client symfony/http-foundation symfony/routing symfony/framework-bundle symfony/dotenv --no-interaction; \
    fi

# Final runtime image
FROM base AS runtime

# Keep the built template separate to support bind-mounting an empty /app on first run
WORKDIR /opt/app-template
COPY --from=builder /src/ .

# Runtime working dir is /app (bind-mounted in docker-compose)
WORKDIR /app

# On container start: if /app has no composer.json (empty volume), seed it from the template, then run the server
EXPOSE 8080
CMD ["sh", "-c", "if [ ! -f /app/composer.json ]; then echo 'Seeding Symfony app into /app...' && cp -R /opt/app-template/. /app && composer install --no-dev --optimize-autoloader --no-interaction; fi; php -S 0.0.0.0:8080 -t public"]
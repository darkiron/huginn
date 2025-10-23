# Laravel Frontend

Location: apps/laravel-front

Overview
- Web UI built with Laravel. Communicates with the Symfony backend.

Local development
- Ensure PHP, Composer, and a DB are available if running natively.
- cp .env.example .env (if available) or edit .env; then run: php artisan key:generate
- composer install
- php artisan migrate (if database is required)
- php artisan serve

Environment highlights
- APP_KEY must be set.
- Configure backend API endpoint via env if applicable.

Testing
- Run PHPUnit tests: php artisan test

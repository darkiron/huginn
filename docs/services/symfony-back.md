# Symfony Backend

Location: apps/symfony-back

Overview
- Provides API endpoints for the application and orchestrates domain logic.
- Key domain elements include Prompt, LLMGateway, and GenerateStreamUseCase.

Key files
- src/Domain/Model/Prompt.php — prompt value object/model
- src/Domain/Port/LLMGateway.php — port for LLM interactions
- src/Application/UseCase/GenerateStreamUseCase.php — streaming generation use case
- src/Controller/LLMController.php — HTTP controller exposing LLM endpoints

Local development
- Copy .env to .env.local and set APP_SECRET.
- composer install
- Run server: symfony server:start or php -S localhost:8000 -t public

Testing
- Use phpunit or Symfony test tools. Tests reside under apps/symfony-back/tests.

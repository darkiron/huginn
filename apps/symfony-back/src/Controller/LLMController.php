<?php

namespace App\Controller;

use App\Application\UseCase\GenerateStreamUseCase;
use Symfony\Component\HttpFoundation\JsonResponse;
use Symfony\Component\HttpFoundation\Request;
use Symfony\Component\HttpFoundation\Response;
use Symfony\Component\Routing\Annotation\Route;

final class LLMController
{
    public function __construct(private readonly GenerateStreamUseCase $useCase) {}

    #[Route(path: '/api/llm/stream', name: 'api_llm_stream', methods: ['POST'])]
    public function stream(Request $request): Response
    {
        $data = json_decode($request->getContent() ?: '[]', true);
        if (!is_array($data)) {
            return new JsonResponse(['error' => 'Invalid JSON payload'], 400);
        }

        $prompt = $data['prompt'] ?? null;
        unset($data['prompt']); // remaining fields are options forwarded to LLM

        try {
            return $this->useCase->execute((string)$prompt, $data);
        } catch (\InvalidArgumentException $e) {
            return new JsonResponse(['error' => $e->getMessage()], 422);
        } catch (\Throwable $e) {
            return new JsonResponse(['error' => 'Streaming failed', 'details' => $e->getMessage()], 502);
        }
    }
}

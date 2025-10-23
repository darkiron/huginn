<?php

namespace App\Infrastructure\LLM;

use App\Domain\Model\Prompt;
use App\Domain\Port\LLMGateway;
use Symfony\Component\DependencyInjection\ParameterBag\ParameterBagInterface;
use Symfony\Contracts\HttpClient\HttpClientInterface;

final class PythonLLMClient implements LLMGateway
{
    public function __construct(
        private readonly HttpClientInterface $httpClient,
        private readonly ParameterBagInterface $params
    ) {}

    /**
     * @inheritDoc
     */
    public function streamGenerate(Prompt $prompt, array $options = []): \Generator
    {
        $url = (string) ($this->params->get('llm_url') ?? getenv('LLM_URL') ?: 'http://llm:8008/generate/stream');

        $payload = array_merge($options, [
            'prompt' => $prompt->value(),
        ]);

        // Issue the request without buffering to enable streaming
        $response = $this->httpClient->request('POST', $url, [
            'json' => $payload,
            'timeout' => 0, // no timeout for long streams
            'buffer' => false,
        ]);

        foreach ($this->httpClient->stream($response) as $chunk) {
            if ($chunk->isTimeout()) {
                // ignore timeouts to keep connection alive
                continue;
            }
            if ($chunk->isFirst()) {
                // you could yield headers if needed
            }
            if ($chunk->isLast()) {
                break;
            }
            if ($chunk->getError()) {
                // Bubble up the error
                throw new \RuntimeException('LLM stream error: '.$chunk->getError());
            }
            $content = $chunk->getContent(false);
            if ($content !== '') {
                yield $content;
            }
        }
    }
}

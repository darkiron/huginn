<?php

namespace App\Application\UseCase;

use App\Domain\Model\Prompt;
use App\Domain\Port\LLMGateway;
use Symfony\Component\HttpFoundation\StreamedResponse;

final class GenerateStreamUseCase
{
    public function __construct(private readonly LLMGateway $llm) {}

    /**
     * @param string $promptText
     * @param array<string,mixed> $options
     */
    public function execute(string $promptText, array $options = []): StreamedResponse
    {
        $prompt = Prompt::fromString($promptText);

        $generator = $this->llm->streamGenerate($prompt, $options);

        $callback = static function () use ($generator): void {
            // FastCGI buffers can prevent real streaming; try disabling if present
            // We still flush after each chunk.
            if (function_exists('apache_setenv')) {
                @apache_setenv('no-gzip', '1');
            }
            @ini_set('zlib.output_compression', '0');
            @ini_set('output_buffering', 'off');
            @ini_set('implicit_flush', '1');
            while (ob_get_level() > 0) {
                @ob_end_flush();
            }
            ob_implicit_flush(true);

            foreach ($generator as $chunk) {
                echo $chunk;
                flush();
            }
        };

        $response = new StreamedResponse($callback, 200, [
            'Content-Type' => 'text/plain; charset=utf-8',
            'Cache-Control' => 'no-cache, no-transform',
            'X-Accel-Buffering' => 'no',
            'Transfer-Encoding' => 'chunked',
        ]);

        return $response;
    }
}

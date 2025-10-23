<?php

namespace App\Domain\Port;

use App\Domain\Model\Prompt;

interface LLMGateway
{
    /**
     * Returns a generator that yields string chunks streamed from the LLM.
     *
     * @param Prompt $prompt
     * @param array<string,mixed> $options Additional payload fields to forward (e.g., temperature)
     * @return \Generator<string>
     */
    public function streamGenerate(Prompt $prompt, array $options = []): \Generator;
}

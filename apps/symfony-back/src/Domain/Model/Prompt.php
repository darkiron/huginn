<?php

namespace App\Domain\Model;

final class Prompt
{
    public function __construct(private readonly string $value) {}

    public static function fromString(?string $value): self
    {
        $trimmed = trim((string) $value);
        if ($trimmed === '') {
            throw new \InvalidArgumentException('Prompt must be a non-empty string.');
        }
        return new self($trimmed);
    }

    public function value(): string
    {
        return $this->value;
    }
}

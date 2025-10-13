@props(['role' => 'assistant', 'text' => ''])
@php
    $isUser = $role === 'user';
@endphp
<div class="card" style="padding:10px 12px;white-space:pre-wrap; border-color:{{ $isUser ? '#0f5132' : 'var(--border)' }}; background:{{ $isUser ? '#0f1f18' : 'var(--card)' }}">
    <div class="muted" style="font-size:12px;margin-bottom:4px">{{ $isUser ? 'You' : 'Assistant' }}</div>
    <div>{{ $text }}</div>
</div>

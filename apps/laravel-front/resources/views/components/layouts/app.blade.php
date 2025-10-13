<!doctype html>
<html lang="fr">
<head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width,initial-scale=1" />
    <title>{{ $title ?? 'Huginn • Chat' }}</title>
    <style>
        :root{--bg:#0b0b0b;--fg:#eaeaea;--muted:#9aa0a6;--card:#141414;--border:#2a2a2a;--accent:#10b981}
        *{box-sizing:border-box} body{margin:0;background:var(--bg);color:var(--fg);font:16px/1.5 system-ui}
        .wrap{max-width:820px;margin:0 auto;padding:16px}
        .card{background:var(--card);border:1px solid var(--border);border-radius:12px}
        .muted{color:var(--muted)}
        .row{display:flex;gap:8px}
        .hidden{display:none}
        .btn{padding:0 16px;height:52px;border-radius:10px;border:1px solid #0d5e44;background:var(--accent);color:#062d1f;font-weight:700}
        textarea{flex:1;min-height:52px;max-height:180px;resize:vertical;border-radius:12px;border:1px solid var(--border);background:#0e0e0e;color:var(--fg);padding:10px}
    </style>
    @stack('head')
</head>
<body>
{{ $slot }}
@stack('scripts')
</body>
</html>

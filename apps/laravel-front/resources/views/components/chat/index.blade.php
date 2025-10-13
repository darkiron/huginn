<x-layouts.app :title="'Huginn • Chat'">
    <x-ui.header />
    <x-ui.container>
        <x-chat.messages />
    </x-ui.container>
    <x-chat.input />

    @push('scripts')
        <script>
            const $msgs = document.getElementById('messages');
            const $form = document.getElementById('chatForm');
            const $input = document.getElementById('prompt');

            const addMsg = (text, role) => {
                const tpl = document.createElement('template');
                tpl.innerHTML = `<div class="card" style="padding:10px 12px;white-space:pre-wrap; border-color:${role==='user'?'#0f5132':'var(--border)'}; background:${role==='user'?'#0f1f18':'var(--card)'}">
        <div class="muted" style="font-size:12px;margin-bottom:4px">${role==='user'?'You':'Assistant'}</div>
        <div>${text.replace(/</g,'&lt;')}</div>
      </div>`;
                $msgs.appendChild(tpl.content.firstElementChild);
                window.scrollTo({ top: document.body.scrollHeight, behavior: 'smooth' });
            };

            $form.addEventListener('submit', async (e) => {
                e.preventDefault();
                const text = $input.value.trim();
                if (!text) return;
                addMsg(text, 'user');
                $input.value = '';

                // Stub Phase 1 (remplaçable par un fetch vers Symfony/LLM plus tard)
                await new Promise(r => setTimeout(r, 250));
                addMsg('Stub • ' + text, 'assistant');
            });
        </script>
    @endpush
</x-layouts.app>

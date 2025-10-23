# LLM RNN CLI — Text Generation via Docker Compose ✨

Cette page explique comment générer du texte avec le modèle RNN depuis le conteneur llm, via la CLI llm_rnn.generate. 🧠🐳

---

Sommaire
- TL;DR rapide ⚡
- Commandes complètes (PowerShell/Bash) 🖥️
- Ce que fait la commande 🔍
- Options de la CLI ⚙️
- Exemples utiles 🧪
- Exécuter hors Docker (avancé) 🚀
- Fichiers et volumes 📁
- Dépannage 🛟
- API et métriques 🌐📈
- Annexes 📚

---

TL;DR ⚡

PowerShell (Windows)

```powershell
PS C:\Users\vincent\huginn> docker compose exec llm /opt/venv/bin/python -m llm_rnn.generate `
  --ckpt /ckpts/rnn.pt `
  --seed "Le soleil se lève sur les collines et" `
  --chars 200 --temp 0.8 --top-p 0.9
```

Bash (macOS/Linux)

```bash
docker compose exec llm /opt/venv/bin/python -m llm_rnn.generate \
  --ckpt /ckpts/rnn.pt \
  --seed "Le soleil se lève sur les collines et" \
  --chars 200 --temp 0.8 --top-p 0.9
```

Ce que ça fait 🔍
- docker compose exec llm … exécute la commande dans le conteneur llm (voir compose.yaml).
- /opt/venv/bin/python -m llm_rnn.generate lance l’entrée CLI du package.
- --ckpt /ckpts/rnn.pt pointe vers le checkpoint monté depuis ./ckpts de l’hôte.

Options de la CLI ⚙️
Implémentation : apps/python-llm/llm_rnn/generate.py
- --ckpt PATH : chemin du checkpoint (.pt). Défaut : /ckpts/rnn.pt
- --seed TEXT : texte d’amorçage (optionnel). Défaut : vide
- --chars INT : nombre de caractères générés. Défaut : 200
- --temp FLOAT : température (plus haut = plus aléatoire). Défaut : 0.9
- --top-k INT : coupe top‑k (optionnel). Défaut : None
- --top-p FLOAT : nucleus/top‑p (optionnel). Défaut : None

Exemples utiles 🧪
1) Échantillon rapide (défauts : /ckpts/rnn.pt, 200 chars, temp=0.9)

```powershell
PS> docker compose exec llm /opt/venv/bin/python -m llm_rnn.generate --seed "Hello world"
```

2) Sortie plus déterministe (temp plus basse, sans nucleus)

```powershell
PS> docker compose exec llm /opt/venv/bin/python -m llm_rnn.generate `
  --seed "Once upon a time" `
  --chars 400 `
  --temp 0.6
```

3) Utiliser top‑k au lieu de top‑p

```bash
docker compose exec llm /opt/venv/bin/python -m llm_rnn.generate \
  --seed "Il était une fois" \
  --chars 300 --temp 0.8 --top-k 50
```

Exécuter hors Docker (avancé) 🚀
Si votre environnement local a Python + PyTorch et que le package est accessible (PYTHONPATH=/app/apps/python-llm dans l’image), vous pouvez lancer :

```bash
python -m llm_rnn.generate --ckpt ./ckpts/rnn.pt --seed "Example" --chars 200
```

Assurez‑vous que llm_rnn (apps/python-llm) est sur le PYTHONPATH, ou installez‑le en package si vous avez une configuration prévue.

Fichiers et volumes 📁
- Checkpoint : ./ckpts/rnn.pt (hôte) monté en /ckpts/rnn.pt (conteneur). compose.yaml : ./ckpts:/ckpts
- Code : ./apps/python-llm monté en /app/apps/python-llm, avec PYTHONPATH=/app/apps/python-llm pour python -m llm_rnn.generate

Dépannage 🛟
- ModuleNotFoundError: No module named 'llm_rnn'
  - Exécutez dans le conteneur (docker compose exec llm …) où PYTHONPATH est défini.
  - En local, définissez PYTHONPATH=apps/python-llm ou installez le package.
- FileNotFoundError: /ckpts/rnn.pt
  - Vérifiez l’existence de ./ckpts/rnn.pt et le volume ./ckpts:/ckpts dans compose.yaml.
  - Changez --ckpt si nécessaire (ex. : un chemin dans /app/…).
- Sortie « bizarre » ou caractères inattendus
  - Baissez --temp vers 0.6–0.8.
  - Assurez la compatibilité tokenizer/checkpoint (byte/BPE). Le loader détecte le type via la config sauvegardée.

API et métriques 🌐📈
- HTTP API : le backend Symfony s’attend à http://llm:8008/generate/stream (voir apps/symfony-back/src/Infrastructure/LLM/PythonLLMClient.php). La CLI ci‑dessus est pratique pour des tests directs.
- Métriques : http://localhost:9108/metrics exposé par services/llm/metrics_server.py (dans le conteneur : /metrics sur 9108).

Annexes 📚
- Entrée CLI : apps/python-llm/llm_rnn/generate.py
- Modèle : apps/python-llm/llm_rnn/model.py (CharRNN + sampling)
- Tokenizers : apps/python-llm/llm_rnn/tokenizer.py et tokenizer_bpe.py

# LLM RNN CLI — Text Generation via Docker Compose

This page documents how to run the character-level RNN generator from inside the llm service container, using the llm_rnn.generate CLI.

The examples below match this command template:

PowerShell (Windows)

PS C:\Users\vincent\huginn> docker compose exec llm /opt/venv/bin/python -m llm_rnn.generate `
  --ckpt /ckpts/rnn.pt `
  --seed "Le soleil se lève sur les collines et" `
  --chars 200 --temp 0.8 --top-p 0.9

Bash (macOS/Linux)

docker compose exec llm /opt/venv/bin/python -m llm_rnn.generate \
  --ckpt /ckpts/rnn.pt \
  --seed "Le soleil se lève sur les collines et" \
  --chars 200 --temp 0.8 --top-p 0.9

What this does
- docker compose exec llm … executes the command inside the llm container defined in compose.yaml.
- /opt/venv/bin/python -m llm_rnn.generate runs the packaged CLI entry point.
- --ckpt /ckpts/rnn.pt points to the pretrained checkpoint mounted from ./ckpts on your host.

Options reference
The generator CLI is implemented in apps/python-llm/llm_rnn/generate.py and supports:
- --ckpt PATH: Path to the model checkpoint (.pt). Default: /ckpts/rnn.pt
- --seed TEXT: Optional seed text to prime the model. Default: empty
- --chars INT: Number of output characters to generate. Default: 200
- --temp FLOAT: Sampling temperature (higher = more random). Default: 0.9
- --top-k INT: Top‑k sampling cutoff (optional). Default: None
- --top-p FLOAT: Top‑p (nucleus) sampling threshold (optional). Default: None

Additional examples
1) Quick sample with defaults (uses /ckpts/rnn.pt, 200 chars, temp=0.9):

PS> docker compose exec llm /opt/venv/bin/python -m llm_rnn.generate --seed "Hello world"

2) Deterministic/safer output (lower temp, no nucleus):

PS> docker compose exec llm /opt/venn/bin/python -m llm_rnn.generate `
  --seed "Once upon a time" `
  --chars 400 `
  --temp 0.6

3) Use top‑k instead of top‑p:

$ docker compose exec llm /opt/venv/bin/python -m llm_rnn.generate \
  --seed "Il était une fois" \
  --chars 300 --temp 0.8 --top-k 50

Running outside Docker (advanced)
If you activated the environment inside the container image layout (PYTHONPATH=/app/apps/python-llm), you can run from the repo on a machine with Python and PyTorch installed:

python -m llm_rnn.generate --ckpt ./ckpts/rnn.pt --seed "Example" --chars 200

Make sure the llm_rnn package (apps/python-llm) is on PYTHONPATH, or install it as a package if you have a setup for that.

Files and volumes
- Checkpoint: ./ckpts/rnn.pt on host is mounted to /ckpts/rnn.pt in the container (compose.yaml mounts ./ckpts:/ckpts).
- Code: ./apps/python-llm is mounted to /app/apps/python-llm; compose sets PYTHONPATH=/app/apps/python-llm so python -m llm_rnn.generate works.

Troubleshooting
- ModuleNotFoundError: No module named 'llm_rnn'
  - Ensure you’re running inside the container (docker compose exec llm …) where PYTHONPATH is set.
  - If running locally, set PYTHONPATH to apps/python-llm or install the package.
- FileNotFoundError: /ckpts/rnn.pt
  - Verify that ./ckpts/rnn.pt exists on your host and the volume ./ckpts:/ckpts is present in compose.yaml.
  - You can change --ckpt to another path in the container (e.g., /app/apps/python-llm/rnn.pt if you placed it there).
- Garbled output or strange characters
  - Try lowering --temp to 0.6–0.8.
  - If your checkpoint was trained with a specific tokenizer (byte/BPE), be sure you’re using the matching checkpoint (the loader auto‑detects kind via the stored config).

Notes about APIs and metrics
- HTTP API: The Symfony backend expects an endpoint like http://llm:8008/generate/stream (see apps/symfony-back/src/Infrastructure/LLM/PythonLLMClient.php). If you need an HTTP generator, implement and run it inside the llm service; the CLI above already works for direct generation.
- Metrics: The llm container exposes Prometheus metrics at http://localhost:9108/metrics (inside the container: /metrics on port 9108), driven by services/llm/metrics_server.py.

Appendix: Where the CLI lives
- Entry point: apps/python-llm/llm_rnn/generate.py
- Model: apps/python-llm/llm_rnn/model.py (CharRNN and sampling)
- Tokenizers: apps/python-llm/llm_rnn/tokenizer.py and tokenizer_bpe.py

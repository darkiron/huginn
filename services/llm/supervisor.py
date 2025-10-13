import threading, os, time
from metrics_server import run as run_metrics

def run_idle():
    # Ici, on garde le conteneur vivant (tu peux remplacer par une boucle IPC/server)
    while True:
        time.sleep(3600)

if __name__ == "__main__":
    t = threading.Thread(target=run_metrics, kwargs={"port": int(os.getenv("METRICS_PORT","9108"))}, daemon=True)
    t.start()
    run_idle()

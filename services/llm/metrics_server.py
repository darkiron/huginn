from http.server import BaseHTTPRequestHandler, HTTPServer
from prometheus_client import CollectorRegistry, Gauge, generate_latest, CONTENT_TYPE_LATEST
import psutil, os, time

class Metrics:
    def __init__(self):
        self.registry = CollectorRegistry()
        self.cpu = Gauge('container_cpu_percent', 'CPU usage percent', registry=self.registry)
        self.mem = Gauge('container_memory_bytes', 'RSS memory bytes', registry=self.registry)
        self.vmem = Gauge('container_virtual_memory_bytes', 'VMS memory bytes', registry=self.registry)
        self.uptime = Gauge('container_uptime_seconds', 'Uptime', registry=self.registry)
        self._start = time.time()
    def collect(self):
        p = psutil.Process(os.getpid())
        self.cpu.set(psutil.cpu_percent(interval=None))
        mi = p.memory_info()
        self.mem.set(mi.rss)
        self.vmem.set(mi.vms)
        self.uptime.set(time.time() - self._start)

metrics = Metrics()

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path != '/metrics':
            self.send_response(404); self.end_headers(); return
        metrics.collect()
        out = generate_latest(metrics.registry)
        self.send_response(200)
        self.send_header('Content-Type', CONTENT_TYPE_LATEST)
        self.send_header('Content-Length', str(len(out)))
        self.end_headers()
        self.wfile.write(out)

def run(port:int=9108):
    HTTPServer(('0.0.0.0', port), Handler).serve_forever()

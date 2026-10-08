"""A tiny status service: GET / returns JSON, GET /health for the container health check."""
import json
import os
import signal
import sys
from http.server import BaseHTTPRequestHandler, HTTPServer


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/health":
            body, code = b"ok", 200
        elif self.path == "/":
            body = json.dumps({"service": "race-status", "uid": os.getuid(),
                               "version": os.environ.get("APP_VERSION", "dev")}).encode()
            code = 200
        else:
            body, code = b"not found", 404
        self.send_response(code)
        self.send_header("Content-Type", "application/json" if self.path == "/" else "text/plain")
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, *args):          # keep CI output clean
        pass


if __name__ == "__main__":
    # As PID 1 in a container, Python gets no default SIGTERM handling: exit cleanly on stop.
    signal.signal(signal.SIGTERM, lambda *_: sys.exit(0))
    HTTPServer(("0.0.0.0", int(os.environ.get("PORT", "8080"))), Handler).serve_forever()

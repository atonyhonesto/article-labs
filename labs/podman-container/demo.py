"""Lint both Containerfiles, then call the service in-process (the container run happens in ci.sh)."""
import json
import subprocess
import sys
import threading
import urllib.request
from http.server import HTTPServer

from app import Handler

subprocess.run([sys.executable, "lint.py", "Containerfile", "samples/Containerfile.bad"])
srv = HTTPServer(("127.0.0.1", 0), Handler)
threading.Thread(target=srv.serve_forever, daemon=True).start()
base = f"http://127.0.0.1:{srv.server_port}"
print("\nGET /health ->", urllib.request.urlopen(base + "/health").read().decode())
print("GET /       ->", json.loads(urllib.request.urlopen(base + "/").read()))
srv.shutdown()

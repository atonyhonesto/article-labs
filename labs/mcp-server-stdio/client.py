"""A tiny MCP client: launches the server as a subprocess and talks JSON-RPC over its stdio."""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


class StdioClient:
    def __init__(self, server: Path):
        self.proc = subprocess.Popen([sys.executable, str(server)], stdin=subprocess.PIPE,
                                     stdout=subprocess.PIPE, text=True, bufsize=1)
        self._id = 0

    def request(self, method: str, params: dict | None = None) -> dict:
        self._id += 1
        self.proc.stdin.write(json.dumps({"jsonrpc": "2.0", "id": self._id, "method": method,
                                          "params": params or {}}) + "\n")
        self.proc.stdin.flush()
        return json.loads(self.proc.stdout.readline())

    def notify(self, method: str) -> None:
        self.proc.stdin.write(json.dumps({"jsonrpc": "2.0", "method": method}) + "\n")
        self.proc.stdin.flush()

    def close(self) -> None:
        self.proc.stdin.close()
        self.proc.wait(timeout=5)

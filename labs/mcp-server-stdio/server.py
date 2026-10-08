"""A minimal Model Context Protocol (MCP) server over stdio, standard library only.

MCP is JSON-RPC 2.0. Over the stdio transport each message is one line of JSON.
This server implements the handshake (`initialize`), tool discovery (`tools/list`)
and tool execution (`tools/call`) over a small race-results dataset, which is
enough for Claude Code or any MCP client to use it.

Register with Claude Code:  claude mcp add race-data -- python /path/to/server.py
"""
from __future__ import annotations

import csv
import json
import sys
from pathlib import Path

PROTOCOL_VERSION = "2025-06-18"
DATA = Path(__file__).with_name("laps.csv")
LOG = sys.stderr                     # stdout carries the protocol; logs go to stderr


def load_laps() -> list[dict]:
    with DATA.open(newline="") as fh:
        return [{"car": r["car"], "lap": int(r["lap"]), "time_s": float(r["time_s"])} for r in csv.DictReader(fh)]


TOOLS = [
    {"name": "list_cars", "description": "List the car numbers in the dataset.",
     "inputSchema": {"type": "object", "properties": {}, "additionalProperties": False}},
    {"name": "best_lap", "description": "Fastest lap and time for one car.",
     "inputSchema": {"type": "object", "properties": {"car": {"type": "string"}},
                     "required": ["car"], "additionalProperties": False}},
    {"name": "average_pace", "description": "Average lap time per car over a lap range, slowest last.",
     "inputSchema": {"type": "object",
                     "properties": {"from_lap": {"type": "integer", "minimum": 1},
                                    "to_lap": {"type": "integer", "minimum": 1}},
                     "required": ["from_lap", "to_lap"], "additionalProperties": False}},
]


def call_tool(name: str, args: dict) -> str:
    laps = load_laps()
    if name == "list_cars":
        return json.dumps(sorted({l["car"] for l in laps}, key=int))
    if name == "best_lap":
        mine = [l for l in laps if l["car"] == str(args["car"])]
        if not mine:
            raise ValueError(f"no laps for car {args['car']}")
        best = min(mine, key=lambda l: l["time_s"])
        return json.dumps({"car": best["car"], "lap": best["lap"], "time_s": best["time_s"]})
    if name == "average_pace":
        lo, hi = int(args["from_lap"]), int(args["to_lap"])
        if lo > hi:
            raise ValueError("from_lap must be <= to_lap")
        by_car: dict[str, list[float]] = {}
        for l in laps:
            if lo <= l["lap"] <= hi:
                by_car.setdefault(l["car"], []).append(l["time_s"])
        rows = sorted(({"car": c, "avg_s": round(sum(v) / len(v), 3), "laps": len(v)} for c, v in by_car.items()),
                      key=lambda r: r["avg_s"])
        return json.dumps(rows)
    raise KeyError(name)


def handle(msg: dict) -> dict | None:
    method, mid = msg.get("method"), msg.get("id")
    if mid is None:                                  # notification (e.g. notifications/initialized)
        return None
    try:
        if method == "initialize":
            result = {"protocolVersion": PROTOCOL_VERSION,
                      "capabilities": {"tools": {"listChanged": False}},
                      "serverInfo": {"name": "race-data", "version": "1.0.0"}}
        elif method == "tools/list":
            result = {"tools": TOOLS}
        elif method == "tools/call":
            params = msg.get("params", {})
            try:
                text = call_tool(params["name"], params.get("arguments", {}))
                result = {"content": [{"type": "text", "text": text}], "isError": False}
            except KeyError as e:
                return {"jsonrpc": "2.0", "id": mid, "error": {"code": -32602, "message": f"unknown tool {e}"}}
            except ValueError as e:                  # tool-level failure: reported to the model, not a protocol error
                result = {"content": [{"type": "text", "text": str(e)}], "isError": True}
        elif method == "ping":
            result = {}
        else:
            return {"jsonrpc": "2.0", "id": mid, "error": {"code": -32601, "message": f"method not found: {method}"}}
        return {"jsonrpc": "2.0", "id": mid, "result": result}
    except Exception as e:                           # never crash the transport
        print(f"internal error: {e!r}", file=LOG)
        return {"jsonrpc": "2.0", "id": mid, "error": {"code": -32603, "message": "internal error"}}


def main() -> None:
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            msg = json.loads(line)
        except json.JSONDecodeError:
            reply = {"jsonrpc": "2.0", "id": None, "error": {"code": -32700, "message": "parse error"}}
        else:
            reply = handle(msg)
        if reply is not None:
            sys.stdout.write(json.dumps(reply) + "\n")
            sys.stdout.flush()


if __name__ == "__main__":
    main()

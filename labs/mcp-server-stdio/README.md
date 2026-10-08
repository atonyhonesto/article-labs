<sub>[← all labs](../../README.md)</sub>

# An MCP server over stdio, from scratch

> MCP is just JSON-RPC 2.0 with a handshake. Here it is with nothing hidden behind an SDK.

`Python` · `MCP` · `JSON-RPC`

**Companion to:**
- [Claude Code MCPs](https://www.linkedin.com/pulse/claude-code-mcps-tony-honesto-v3loc/)

## What it shows

- The three messages every MCP server needs: `initialize`, `tools/list` and `tools/call`.
- Tools described with JSON Schema so a model knows exactly what arguments to send.
- The difference between a protocol error (unknown method → JSON-RPC error) and a tool error (`isError: true`, returned to the model so it can recover).
- Logs go to stderr, because stdout carries the protocol.
- A tiny client that launches the server as a subprocess, the same way Claude Code does.

## Run it

```bash
bash labs/mcp-server-stdio/ci.sh
# use it from Claude Code:
claude mcp add race-data -- python /absolute/path/to/labs/mcp-server-stdio/server.py
```

Real output:

```text
Server: {'name': 'race-data', 'version': '1.0.0'} protocol 2025-06-18
Tools:  ['list_cars', 'best_lap', 'average_pace']
best_lap({"car": "24"}) -> isError=False {"car": "24", "lap": 7, "time_s": 30.957}
average_pace({"from_lap": 10, "to_lap": 20}) -> isError=False [{"car": "5", "avg_s": 31.087, "laps": 11}, {"car": "24", "avg_s": 31.201, "laps": 11}, {"car": "11", "avg_s": 31.253, "laps": 11}, {"car": "48", "avg_s": 31.355, "laps": 11}]
best_lap({"car": "99"}) -> isError=True no laps for car 99
```

## What's in here

| File | Purpose |
|---|---|
| `server.py` | The MCP server: handshake, tool list, tool calls over a lap-time CSV |
| `client.py` | Minimal stdio JSON-RPC client |
| `laps.csv` | 160 laps for four cars |
| `demo.py` | Handshake, discovery and three tool calls |
| `tests/` | Protocol and tool-error tests |

## Simulated here vs. a real deployment

| In this lab | In production |
|---|---|
| Hand-written JSON-RPC | The official MCP Python or C# SDK (see ParquetMCPServer for a .NET version) |
| CSV file | A database, Parquet files or an internal API |
| Three tools | Resources and prompts as well as tools, with auth for remote (HTTP) transports |

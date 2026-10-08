import json
from pathlib import Path

from client import StdioClient

c = StdioClient(Path(__file__).with_name("server.py"))
init = c.request("initialize", {"protocolVersion": "2025-06-18", "capabilities": {},
                                "clientInfo": {"name": "demo", "version": "0"}})
c.notify("notifications/initialized")
print("Server:", init["result"]["serverInfo"], "protocol", init["result"]["protocolVersion"])
print("Tools: ", [t["name"] for t in c.request("tools/list")["result"]["tools"]])
for name, args in (("best_lap", {"car": "24"}), ("average_pace", {"from_lap": 10, "to_lap": 20}),
                   ("best_lap", {"car": "99"})):
    r = c.request("tools/call", {"name": name, "arguments": args})["result"]
    print(f"{name}({json.dumps(args)}) -> isError={r['isError']} {r['content'][0]['text']}")
c.close()

import json
import unittest
from pathlib import Path

from client import StdioClient

SERVER = Path(__file__).resolve().parent.parent / "server.py"


class McpServerTests(unittest.TestCase):
    def setUp(self):
        self.c = StdioClient(SERVER)
        self.c.request("initialize", {"protocolVersion": "2025-06-18", "capabilities": {}, "clientInfo": {"name": "t", "version": "0"}})
        self.c.notify("notifications/initialized")

    def tearDown(self):
        self.c.close()

    def test_tools_have_json_schemas(self):
        tools = self.c.request("tools/list")["result"]["tools"]
        self.assertEqual({t["name"] for t in tools}, {"list_cars", "best_lap", "average_pace"})
        self.assertTrue(all(t["inputSchema"]["type"] == "object" for t in tools))

    def test_best_lap(self):
        r = self.c.request("tools/call", {"name": "best_lap", "arguments": {"car": "5"}})["result"]
        self.assertFalse(r["isError"])
        self.assertEqual(json.loads(r["content"][0]["text"])["car"], "5")

    def test_tool_error_is_reported_to_the_model(self):
        r = self.c.request("tools/call", {"name": "average_pace", "arguments": {"from_lap": 9, "to_lap": 3}})["result"]
        self.assertTrue(r["isError"])

    def test_unknown_method_is_a_protocol_error(self):
        self.assertEqual(self.c.request("resources/list")["error"]["code"], -32601)


if __name__ == "__main__":
    unittest.main()

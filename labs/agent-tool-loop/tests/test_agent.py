import unittest
from agent import Agent, compute_stats, scripted_planner


class AgentTests(unittest.TestCase):
    def test_stats(self):
        s = compute_stats("RACE")
        self.assertEqual(s["return_pct"], 24.0)
        self.assertLess(s["max_drawdown_pct"], 0)

    def test_tool_errors_are_recorded_not_raised(self):
        a = Agent(scripted_planner)
        report = a.run("Analyse NOPE")
        self.assertIn("could not analyse", report)
        self.assertFalse(a.trail[0]["ok"])

    def test_step_budget_stops_runaway_loops(self):
        loop = lambda goal, trail: {"type": "tool", "tool": "get_prices", "args": {"ticker": "RACE"}}
        a = Agent(loop, max_steps=3)
        self.assertIn("budget", a.run("x"))
        self.assertEqual(len(a.trail), 3)


if __name__ == "__main__":
    unittest.main()

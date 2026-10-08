import json

from agent import Agent, scripted_planner

agent = Agent(scripted_planner)
print(agent.run("Compare RACE and PITS, and include FAKE."))
print("\nAudit trail:")
for t in agent.trail:
    print(" ", json.dumps({k: v for k, v in t.items() if k != "result"}))

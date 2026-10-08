import asyncio

from pubsub import PubSub, drain


async def main():
    ps = PubSub()
    team_24 = ps.subscribe("pit-wall-24", "onLapCompleted", car="24")
    leader = ps.subscribe("tv-graphics", "onPositionChanged", position=1)
    everyone = ps.subscribe("data-lake", "onLapCompleted")
    for lap in range(1, 4):
        for car, t in (("24", 31.2), ("5", 31.1), ("48", 31.4)):
            ps.mutate("onLapCompleted", {"car": car, "lap": lap, "time_s": t})
    ps.mutate("onPositionChanged", {"car": "5", "position": 1})
    ps.mutate("onPositionChanged", {"car": "24", "position": 2})
    print(f"{ps.published} mutations published")
    for name, sub in (("pit-wall-24", team_24), ("tv-graphics", leader), ("data-lake", everyone)):
        msgs = await drain(sub)
        print(f"  {name:12} received {len(msgs):2}: {msgs[:2]}{' ...' if len(msgs) > 2 else ''}")

asyncio.run(main())

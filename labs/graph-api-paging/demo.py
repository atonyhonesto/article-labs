from graph import BASE, FakeGraph, delta, get_with_retry, read_all

g = FakeGraph()
try:
    get_with_retry(g, BASE, sleep=lambda s: None)
except RuntimeError as e:
    print("Unfiltered query on 25,000 items ->", e)
waits = []
active = read_all(g, "Active", sleep=waits.append)
print(f"Filtered on an indexed column: {len(active):,} items in {g.calls} calls, "
      f"{len(waits)} throttles honoured (waited {sum(waits):.0f} s)")
_, link = delta(g, None)
g.update([10, 20, 30])
changed, link = delta(g, link)
print(f"Next sync via delta query: {len(changed)} changed items instead of {len(g.items):,}")

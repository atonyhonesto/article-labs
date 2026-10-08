from geotab import FakeServer, GeotabClient

srv = FakeServer()
client = GeotabClient(srv.call, "demo_db", "api@example.com", "demo-password")
rows, version = client.sync_feed("LogRecord", None)
print(f"Initial sync: {len(rows):,} GPS records in {srv.calls.count('GetFeed')} GetFeed pages, saved version {version}")
srv.add(42)
srv.expire_session()
srv.calls.clear()
new, version = client.sync_feed("LogRecord", version)
print(f"Next sync from saved version: {len(new)} new records; calls made: {srv.calls}")

<sub>[← all labs](../../README.md)</sub>

# Incremental Geotab GetFeed client

> Never pull the whole fleet's history twice. Save the version token and ask only for what's new.

`Python` · `stdlib`

**Companion to:**
- [Geotab API Integration](https://www.linkedin.com/pulse/geotab-api-integration-tony-honesto-kzdac/)

## What it shows

- JSON-RPC calls to a Geotab-style API with a session from `Authenticate`.
- `GetFeed` paging with `fromVersion` / `toVersion` tokens until the feed is drained.
- Automatic re-authentication when the session expires (`InvalidUserException`) and a retry of the failed call.
- Resuming from the saved version so the next sync returns only new records.

## Run it

```bash
bash labs/geotab-feed-client/ci.sh        # install, test, run the demo
# or, from this folder:
python demo.py
```

Real output:

```text
Initial sync: 2,350 GPS records in 4 GetFeed pages, saved version 2350
Next sync from saved version: 42 new records; calls made: ['GetFeed', 'Authenticate', 'GetFeed', 'GetFeed']
```

## What's in here

| File | Purpose |
|---|---|
| `geotab.py` | Fake server and client with auth, retry and feed paging |
| `demo.py` | Initial sync, session expiry and incremental sync |
| `tests/` | Paging, re-auth and resume tests |

## Simulated here vs. a real deployment

| In this lab | In production |
|---|---|
| FakeServer | `https://my.geotab.com/apiv1` (or `mygeotab` Python SDK) |
| Version in memory | Version token persisted next to the data it produced |
| Single feed | LogRecord, StatusData and FaultData feeds on a schedule |

<sub>[← all labs](../../README.md)</sub>

# XMPP federation and routing, in miniature

> Email-style addresses, servers that talk to each other, and XML stanzas. XMPP has federated real-time messaging since 1999.

`Python` · `XMPP` · `XML stanzas`

**Companion to:**
- [XMPP — Real-Time, Federated Communication](https://www.linkedin.com/pulse/xmpp-real-time-federated-communication-tony-honesto-rdq1c/)

## What it shows

- JIDs (`local@domain/resource`): the domain picks the server, the resource picks the device.
- Server-to-server (s2s) delivery between two domains, with the domain lookup standing in for DNS SRV records.
- Offline storage: a message to someone who isn't logged in is held and delivered at login.
- Bare-JID routing to the highest-priority resource, and presence only for approved subscribers.
- A stanza whose `from` doesn't match the sending server is dropped (what dialback/SASL enforce).

## Run it

```bash
bash labs/xmpp-routing/ci.sh        # install, test, run the demo
# or, from this folder:
python demo.py
```

Real output:

```text
steward offline -> stored on racecontrol.example: 1 message
steward logs in, offline delivery: ['Requesting review of the T3 incident, car 24']
engineer's laptop sees presence: ['<presence available>']
reply to bare JID -> laptop (priority 5): ['Reviewed: no further action'] | phone (priority 1): []
forged 'from' over s2s dropped: True
s2s hops: [('team24.example', 'racecontrol.example'), ('racecontrol.example', 'team24.example'), ('racecontrol.example', 'team24.example')]
```

## What's in here

| File | Purpose |
|---|---|
| `xmpp.py` | JID parsing, stanzas, servers and federation |
| `demo.py` | An engineer and a race steward on two different servers |
| `tests/` | Routing, offline, priority, presence and spoofing tests |

## Simulated here vs. a real deployment

| In this lab | In production |
|---|---|
| Dict of servers | DNS SRV lookup of `_xmpp-server._tcp.<domain>` |
| Trusted links | TLS plus SASL EXTERNAL or server dialback between servers |
| In-memory stores | ejabberd / Prosody / Openfire with persistent rosters and MAM archives |

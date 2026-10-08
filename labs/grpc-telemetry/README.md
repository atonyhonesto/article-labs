<sub>[← all labs](../../README.md)</sub>

# gRPC telemetry service

> A contract first, binary on the wire, streaming built in, and deadlines on every call.

`Python` · `gRPC` · `Protocol Buffers`

**Companion to:**
- [gRPC Still Matters](https://www.linkedin.com/pulse/grpc-still-matters-tony-honesto-rdexc/)

## What it shows

- A `.proto` contract compiled to Python stubs at build time.
- Unary and server-streaming calls over one HTTP/2 channel.
- Typed status codes (`NOT_FOUND`) instead of ad-hoc error bodies.
- Deadlines: a slow stream is cut off on time, so the client never hangs.
- The same message as protobuf and as JSON, compared by size.

## Run it

```bash
bash labs/grpc-telemetry/ci.sh
# or:
pip install -r requirements.txt
python demo.py
```

Real output (from this lab's CI run):

```text
Unary GetLap: car 24 lap 12 42.016s on SOFT
Same lap on the wire: protobuf 52 bytes vs JSON 124 bytes (2.4x)
Server stream: 10 laps (31-40) over one call
Typed error: NOT_FOUND: no lap 1 for car 99
Deadline: slow stream cut off after 3 laps with DEADLINE_EXCEEDED; the client never hangs
```

## What's in here

| File | Purpose |
|---|---|
| `telemetry.proto` | The service contract |
| `gen.py` | Compiles the stubs (grpc_tools.protoc) |
| `server.py` | Telemetry service |
| `demo.py` | Unary, stream, error and deadline |
| `tests/` | End-to-end tests over a real channel |

## Simulated here vs. a real deployment

| In this lab | In production |
|---|---|
| Insecure local channel | TLS / mTLS, with auth in call metadata |
| Python server | Any language: the same .proto generates C#, Go, Java and TypeScript stubs |
| Direct calls | Load balancing, retries and health checks via a service mesh or gRPC-Web for browsers |

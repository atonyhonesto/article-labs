import json

import grpc
from google.protobuf.json_format import MessageToDict

from server import pb, rpc, serve

server, port = serve()
with grpc.insecure_channel(f"127.0.0.1:{port}") as channel:
    stub = rpc.TelemetryStub(channel)

    lap = stub.GetLap(pb.LapRequest(car="24", lap=12), timeout=2)
    print(f"Unary GetLap: car {lap.car} lap {lap.lap} {lap.lap_time_s:.3f}s on {pb.TyreCompound.Name(lap.tyre)}")

    as_json = json.dumps(MessageToDict(lap)).encode()
    print(f"Same lap on the wire: protobuf {lap.ByteSize()} bytes vs JSON {len(as_json)} bytes "
          f"({len(as_json) / lap.ByteSize():.1f}x)")

    laps = list(stub.StreamLaps(pb.StreamRequest(car="5", from_lap=31), timeout=5))
    print(f"Server stream: {len(laps)} laps ({laps[0].lap}-{laps[-1].lap}) over one call")

    try:
        stub.GetLap(pb.LapRequest(car="99", lap=1), timeout=2)
    except grpc.RpcError as e:
        print(f"Typed error: {e.code().name}: {e.details()}")

    got = 0
    try:
        for _ in stub.StreamLaps(pb.StreamRequest(car="48", from_lap=1, delay_ms=100), timeout=0.35):
            got += 1
    except grpc.RpcError as e:
        print(f"Deadline: slow stream cut off after {got} laps with {e.code().name}; the client never hangs")
server.stop(None)

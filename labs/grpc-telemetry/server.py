"""gRPC server for the Telemetry service, backed by a generated race."""
from __future__ import annotations

import random
import time
from concurrent import futures

import grpc

import gen

gen.ensure()
import telemetry_pb2 as pb          # noqa: E402
import telemetry_pb2_grpc as rpc    # noqa: E402


def race(cars=("5", "24", "48"), laps=40, seed=1):
    rng = random.Random(seed)
    data = {}
    for car in cars:
        for lap in range(1, laps + 1):
            sectors = [round(rng.uniform(13.5, 14.5), 3) for _ in range(3)]
            data[(car, lap)] = pb.Lap(car=car, lap=lap, lap_time_s=round(sum(sectors), 3),
                                      top_speed_kph=round(rng.uniform(318, 334), 1), sector_times_s=sectors,
                                      tyre=pb.SOFT if lap <= 15 else pb.MEDIUM)
    return data


class TelemetryService(rpc.TelemetryServicer):
    def __init__(self):
        self.laps = race()

    def GetLap(self, request, context):
        lap = self.laps.get((request.car, request.lap))
        if lap is None:
            context.abort(grpc.StatusCode.NOT_FOUND, f"no lap {request.lap} for car {request.car}")
        return lap

    def StreamLaps(self, request, context):
        lap = max(1, request.from_lap)
        while (request.car, lap) in self.laps:
            if not context.is_active():          # client cancelled or its deadline passed
                return
            if request.delay_ms:
                time.sleep(request.delay_ms / 1000)
            yield self.laps[(request.car, lap)]
            lap += 1


def serve(port: int = 0) -> tuple[grpc.Server, int]:
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=4))
    rpc.add_TelemetryServicer_to_server(TelemetryService(), server)
    bound = server.add_insecure_port(f"127.0.0.1:{port}")
    server.start()
    return server, bound


if __name__ == "__main__":
    s, p = serve(50051)
    print(f"Telemetry gRPC server on 127.0.0.1:{p}")
    s.wait_for_termination()

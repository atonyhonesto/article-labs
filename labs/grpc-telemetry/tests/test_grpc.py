import unittest

import grpc

from server import pb, rpc, serve


class GrpcTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server, port = serve()
        cls.channel = grpc.insecure_channel(f"127.0.0.1:{port}")
        cls.stub = rpc.TelemetryStub(cls.channel)

    @classmethod
    def tearDownClass(cls):
        cls.channel.close()
        cls.server.stop(None)

    def test_unary(self):
        lap = self.stub.GetLap(pb.LapRequest(car="5", lap=1), timeout=2)
        self.assertEqual((lap.car, lap.lap, len(lap.sector_times_s)), ("5", 1, 3))
        self.assertAlmostEqual(lap.lap_time_s, sum(lap.sector_times_s), places=2)

    def test_not_found_is_a_status_code(self):
        with self.assertRaises(grpc.RpcError) as cm:
            self.stub.GetLap(pb.LapRequest(car="5", lap=999), timeout=2)
        self.assertEqual(cm.exception.code(), grpc.StatusCode.NOT_FOUND)

    def test_stream_order(self):
        laps = [l.lap for l in self.stub.StreamLaps(pb.StreamRequest(car="24", from_lap=35), timeout=5)]
        self.assertEqual(laps, [35, 36, 37, 38, 39, 40])

    def test_deadline(self):
        with self.assertRaises(grpc.RpcError) as cm:
            list(self.stub.StreamLaps(pb.StreamRequest(car="24", from_lap=1, delay_ms=200), timeout=0.3))
        self.assertEqual(cm.exception.code(), grpc.StatusCode.DEADLINE_EXCEEDED)

    def test_protobuf_smaller_than_json(self):
        import json
        from google.protobuf.json_format import MessageToDict
        lap = self.stub.GetLap(pb.LapRequest(car="5", lap=2), timeout=2)
        self.assertLess(lap.ByteSize(), len(json.dumps(MessageToDict(lap))))


if __name__ == "__main__":
    unittest.main()

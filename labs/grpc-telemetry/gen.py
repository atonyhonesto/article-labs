"""Compile telemetry.proto into Python stubs (generated/), the step a build would run."""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE / "generated"


def ensure() -> None:
    if not (OUT / "telemetry_pb2_grpc.py").exists():
        from grpc_tools import protoc
        OUT.mkdir(exist_ok=True)
        rc = protoc.main(["protoc", f"-I{HERE}", f"--python_out={OUT}", f"--grpc_python_out={OUT}", str(HERE / "telemetry.proto")])
        if rc != 0:
            raise SystemExit("protoc failed")
    if str(OUT) not in sys.path:
        sys.path.insert(0, str(OUT))


if __name__ == "__main__":
    ensure()
    print("stubs in", OUT)

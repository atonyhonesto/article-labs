"""A telemetry lake laid out the way S3 likes it, backed here by a local folder.

Keys are partitioned series/season/event/session/car so a prefix answers most
questions without a scan. `sync_team_bucket` copies each team only its own car,
the pattern used to protect competition data.
"""
from __future__ import annotations

import json
import shutil
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Key:
    series: str
    season: int
    event: str
    session: str
    car: str
    lap: int

    def path(self) -> str:
        return (f"series={self.series}/season={self.season}/event={self.event}/"
                f"session={self.session}/car={self.car}/lap={self.lap:03d}.json")


class LocalBucket:
    """Implements the slice of the S3 API this lab needs: put, get, list by prefix, copy."""

    def __init__(self, root: Path):
        self.root = Path(root)
        self.root.mkdir(parents=True, exist_ok=True)

    def put_object(self, key: str, body: dict) -> None:
        p = self.root / key
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(json.dumps(body))

    def get_object(self, key: str) -> dict:
        return json.loads((self.root / key).read_text())

    def list_objects(self, prefix: str = "") -> list[str]:
        return sorted(str(p.relative_to(self.root)).replace("\\", "/")
                      for p in self.root.rglob("*.json")
                      if str(p.relative_to(self.root)).replace("\\", "/").startswith(prefix))

    def copy_to(self, key: str, other: "LocalBucket") -> None:
        dst = other.root / key
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(self.root / key, dst)


def sync_team_bucket(source: LocalBucket, team_bucket: LocalBucket, cars: set[str]) -> int:
    """Copy only the given cars' objects. Returns how many objects were copied."""
    copied = 0
    for key in source.list_objects():
        car = next(part.split("=", 1)[1] for part in key.split("/") if part.startswith("car="))
        if car in cars:
            source.copy_to(key, team_bucket)
            copied += 1
    return copied

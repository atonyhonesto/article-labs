"""Pulling fleet GPS data incrementally, the way the Geotab API is designed to be used.

Geotab's API is JSON-RPC over HTTPS. `Authenticate` returns credentials with a
session id; every call carries them. For large, growing datasets (GPS LogRecords,
StatusData) the right call is `GetFeed`: you pass the `toVersion` from the last
response and get only what is new, in pages, without ever re-reading old data.
When a session expires the server returns `InvalidUserException`; the client
re-authenticates once and retries.

`FakeServer` imitates those behaviours so this runs offline.
"""
from __future__ import annotations

from typing import Callable


class InvalidUser(Exception):
    pass


class FakeServer:
    def __init__(self, records: int = 2350, page: int = 1000):
        self.records = [{"id": f"b{i}", "device": {"id": f"b{i % 7 + 1}"}, "latitude": 39.8 + i * 1e-5,
                         "longitude": -86.2, "speed": (i * 7) % 120, "dateTime": f"2026-05-24T16:{i // 60 % 60:02d}:{i % 60:02d}Z"}
                        for i in range(records)]
        self.page, self.session, self.calls = page, None, []

    def add(self, n: int):
        start = len(self.records)
        self.records += [{"id": f"b{start + i}", "device": {"id": "b1"}, "latitude": 39.9, "longitude": -86.2,
                          "speed": 50, "dateTime": "2026-05-24T17:00:00Z"} for i in range(n)]

    def expire_session(self):
        self.session = None

    def call(self, method: str, params: dict) -> dict:
        self.calls.append(method)
        if method == "Authenticate":
            if params.get("password") != "demo-password":
                raise InvalidUser("bad credentials")
            self.session = "S-" + str(len(self.calls))
            return {"credentials": {"database": params["database"], "userName": params["userName"], "sessionId": self.session}}
        if params.get("credentials", {}).get("sessionId") != self.session or self.session is None:
            raise InvalidUser("session expired")
        if method == "GetFeed":
            start = int(params.get("fromVersion") or 0)
            data = self.records[start:start + min(params.get("resultsLimit", 50000), self.page)]
            return {"data": data, "toVersion": str(start + len(data))}
        raise ValueError(f"unknown method {method}")


class GeotabClient:
    def __init__(self, transport: Callable[[str, dict], dict], database: str, user: str, password: str):
        self.t, self.db, self.user, self.pw = transport, database, user, password
        self.creds = None

    def _auth(self):
        self.creds = self.t("Authenticate", {"database": self.db, "userName": self.user, "password": self.pw})["credentials"]

    def call(self, method: str, **params) -> dict:
        if self.creds is None:
            self._auth()
        try:
            return self.t(method, {**params, "credentials": self.creds})
        except InvalidUser:
            self._auth()                                  # session expired: re-authenticate once, then retry
            return self.t(method, {**params, "credentials": self.creds})

    def sync_feed(self, type_name: str, from_version: str | None) -> tuple[list[dict], str]:
        """Drain the feed from a saved version. Persist the returned version for the next run."""
        out, version = [], from_version
        while True:
            r = self.call("GetFeed", typeName=type_name, fromVersion=version, resultsLimit=50000)
            out += r["data"]
            if not r["data"]:
                return out, r["toVersion"]
            version = r["toVersion"]

"""Reading a very large SharePoint list through Microsoft Graph, the safe way.

Big lists trip three things: the 5,000-item list view threshold, page size limits,
and throttling (HTTP 429 with a Retry-After header). The client here:

* follows `@odata.nextLink` until the last page instead of asking for everything
* filters on an indexed column so the query stays under the view threshold
* honours `Retry-After` on 429/503
* uses a delta query so the next sync only fetches what changed

`FakeGraph` mimics those Graph behaviours so the lab runs offline; the client
code would point at https://graph.microsoft.com/v1.0 unchanged.
"""
from __future__ import annotations

import re
from typing import Callable
from urllib.parse import parse_qs, urlparse

BASE = "https://graph.microsoft.com/v1.0/sites/contoso/lists/RaceParts/items"


class FakeGraph:
    def __init__(self, n_items: int = 25_000, page_size: int = 1000, throttle_every: int = 7):
        self.items = {i: {"id": str(i), "fields": {"Status": "Active" if i % 5 else "Retired", "Part": f"P-{i:05d}"}}
                      for i in range(1, n_items + 1)}
        self.page_size, self.throttle_every, self.calls = page_size, throttle_every, 0
        self.version = 1
        self.changed_at: dict[int, int] = {i: 1 for i in self.items}

    def update(self, ids):
        self.version += 1
        for i in ids:
            self.items[i]["fields"]["Status"] = "Retired"
            self.changed_at[i] = self.version

    def get(self, url: str) -> tuple[int, dict, dict]:
        self.calls += 1
        if self.throttle_every and self.calls % self.throttle_every == 0:
            return 429, {"Retry-After": "2"}, {"error": {"code": "TooManyRequests"}}
        q = parse_qs(urlparse(url).query)
        flt = q.get("$filter", [""])[0]
        if "/delta" in url:
            since = int(q.get("token", ["0"])[0])
            rows = [self.items[i] for i, v in self.changed_at.items() if v > since]
            return 200, {}, {"value": rows, "@odata.deltaLink": f"{BASE}/delta?token={self.version}"}
        if not flt and len(self.items) > 5000:
            return 400, {}, {"error": {"code": "listViewThreshold", "message": "query exceeds the list view threshold"}}
        status = re.search(r"fields/Status eq '(\w+)'", flt).group(1)
        rows = [r for r in self.items.values() if r["fields"]["Status"] == status]
        skip = int(q.get("$skiptoken", ["0"])[0])
        page = rows[skip:skip + self.page_size]
        body = {"value": page}
        if skip + self.page_size < len(rows):
            body["@odata.nextLink"] = f"{BASE}?$filter={flt}&$skiptoken={skip + self.page_size}"
        return 200, {}, body


def get_with_retry(graph, url: str, sleep: Callable[[float], None], max_tries: int = 5) -> dict:
    for _ in range(max_tries):
        status, headers, body = graph.get(url)
        if status == 200:
            return body
        if status in (429, 503):
            sleep(float(headers.get("Retry-After", "1")))
            continue
        raise RuntimeError(f"Graph error {status}: {body['error']['code']}")
    raise RuntimeError("gave up after repeated throttling")


def read_all(graph, status: str, sleep=lambda s: None) -> list[dict]:
    url, out = f"{BASE}?$filter=fields/Status eq '{status}'", []
    while url:
        body = get_with_retry(graph, url, sleep)
        out += body["value"]
        url = body.get("@odata.nextLink")
    return out


def delta(graph, delta_link: str | None, sleep=lambda s: None) -> tuple[list[dict], str]:
    body = get_with_retry(graph, delta_link or f"{BASE}/delta?token=0", sleep)
    return body["value"], body["@odata.deltaLink"]

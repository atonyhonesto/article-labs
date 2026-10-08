"""A tiny model of XMPP federation (RFC 6120 / 6121), enough to see how it routes.

* Addresses are JIDs: local@domain/resource. The domain decides which server owns it.
* Clients talk only to their own server (c2s). Servers talk to each other (s2s),
  found in real life through DNS SRV records (_xmpp-server._tcp.domain).
* Stanzas are XML: <message/>, <presence/>, <iq/>.
* A message to a bare JID goes to the user's highest-priority resource;
  if nobody is online it is stored and delivered when they log in.
* Presence only flows to contacts with an approved subscription.
"""
from __future__ import annotations

from dataclasses import dataclass, field
import xml.etree.ElementTree as ET


@dataclass(frozen=True)
class JID:
    local: str
    domain: str
    resource: str | None = None

    @classmethod
    def parse(cls, text: str) -> "JID":
        resource = None
        if "/" in text:
            text, resource = text.split("/", 1)
        if "@" not in text:
            raise ValueError(f"not a user JID: {text!r}")
        local, domain = text.split("@", 1)
        if not local or not domain:
            raise ValueError(f"bad JID: {text!r}")
        return cls(local.lower(), domain.lower(), resource)   # local + domain are case-insensitive

    @property
    def bare(self) -> "JID":
        return JID(self.local, self.domain)

    def __str__(self) -> str:
        s = f"{self.local}@{self.domain}"
        return f"{s}/{self.resource}" if self.resource else s


def stanza(kind: str, frm: JID, to: JID, body: str | None = None, ptype: str | None = None) -> str:
    el = ET.Element(kind, {"from": str(frm), "to": str(to)})
    if ptype:
        el.set("type", ptype)
    if body is not None:
        ET.SubElement(el, "body").text = body
    return ET.tostring(el, encoding="unicode")


@dataclass
class Network:
    """Stands in for DNS SRV lookup: domain -> server."""
    servers: dict[str, "Server"] = field(default_factory=dict)
    s2s_log: list[tuple[str, str]] = field(default_factory=list)

    def add(self, server: "Server") -> "Server":
        self.servers[server.domain] = server
        server.network = self
        return server

    def deliver_s2s(self, frm_domain: str, xml: str) -> None:
        to = JID.parse(ET.fromstring(xml).get("to"))
        target = self.servers.get(to.domain)
        if target is None:
            raise LookupError(f"remote-server-not-found: {to.domain}")
        self.s2s_log.append((frm_domain, to.domain))
        target.receive(xml, from_remote=frm_domain)


@dataclass
class Server:
    domain: str
    network: Network | None = None
    sessions: dict[JID, dict[str, int]] = field(default_factory=dict)      # bare -> {resource: priority}
    inbox: dict[JID, list[str]] = field(default_factory=dict)              # full JID -> stanzas delivered
    offline: dict[JID, list[str]] = field(default_factory=dict)            # bare -> stored stanzas
    roster: dict[JID, set[JID]] = field(default_factory=dict)              # bare -> who may see my presence

    def login(self, jid: JID, priority: int = 0) -> list[str]:
        assert jid.domain == self.domain and jid.resource
        self.sessions.setdefault(jid.bare, {})[jid.resource] = priority
        self.inbox.setdefault(jid, [])
        waiting = self.offline.pop(jid.bare, [])
        self.inbox[jid].extend(waiting)
        self.broadcast_presence(jid, available=True)
        return waiting

    def logout(self, jid: JID) -> None:
        self.sessions.get(jid.bare, {}).pop(jid.resource, None)
        self.broadcast_presence(jid, available=False)

    def approve(self, owner: JID, contact: JID) -> None:
        """owner lets contact see owner's presence (a 'from' subscription)."""
        self.roster.setdefault(owner.bare, set()).add(contact.bare)

    def broadcast_presence(self, jid: JID, available: bool) -> None:
        for contact in self.roster.get(jid.bare, set()):
            self.send(stanza("presence", jid, contact, ptype=None if available else "unavailable"))

    def send(self, xml: str) -> None:
        """Entry point for stanzas from this server's own clients."""
        to = JID.parse(ET.fromstring(xml).get("to"))
        if to.domain == self.domain:
            self.receive(xml)
        else:
            self.network.deliver_s2s(self.domain, xml)

    def receive(self, xml: str, from_remote: str | None = None) -> None:
        el = ET.fromstring(xml)
        frm, to = JID.parse(el.get("from")), JID.parse(el.get("to"))
        if from_remote and frm.domain != from_remote:
            return                                  # spoofed 'from': drop it (server dialback/SASL in real life)
        resources = self.sessions.get(to.bare, {})
        if el.tag == "presence":
            for res in resources:                   # presence goes to every online resource
                self.inbox[JID(to.local, to.domain, res)].append(xml)
            return
        if to.resource and to.resource in resources:
            self.inbox[to].append(xml)
        elif resources:
            best = max(resources, key=lambda r: resources[r])
            self.inbox[JID(to.local, to.domain, best)].append(xml)
        else:
            self.offline.setdefault(to.bare, []).append(xml)

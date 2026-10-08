import xml.etree.ElementTree as ET
from xmpp import JID, Network, Server, stanza


def bodies(items):
    return [ET.fromstring(x).findtext("body") or f"<{ET.fromstring(x).tag} {ET.fromstring(x).get('type') or 'available'}>" for x in items]


net = Network()
team = net.add(Server("team24.example"))
race = net.add(Server("racecontrol.example"))

engineer_laptop = JID.parse("engineer@team24.example/laptop")
engineer_phone = JID.parse("engineer@team24.example/phone")
steward = JID.parse("steward@racecontrol.example/desk")

team.login(engineer_laptop, priority=5)
team.login(engineer_phone, priority=1)

# The steward is offline: the message crosses servers and is stored.
team.send(stanza("message", engineer_laptop, steward.bare, "Requesting review of the T3 incident, car 24"))
print("steward offline -> stored on racecontrol.example:", len(race.offline[steward.bare]), "message")

race.approve(steward, engineer_laptop)          # steward lets the engineer see presence
waiting = race.login(steward, priority=0)
print("steward logs in, offline delivery:", bodies(waiting))
print("engineer's laptop sees presence:", bodies(team.inbox[engineer_laptop]))

# Reply to the bare JID: goes to the highest-priority resource only.
race.send(stanza("message", steward, engineer_laptop.bare, "Reviewed: no further action"))
msgs = lambda j: [b for b in bodies(team.inbox[j]) if not b.startswith("<")]
print("reply to bare JID -> laptop (priority 5):", msgs(engineer_laptop), "| phone (priority 1):", msgs(engineer_phone))

# A forged stanza claiming to be from racecontrol, arriving over team24's s2s link, is dropped.
race.receive(stanza("message", JID.parse("chief@racecontrol.example"), steward.bare, "forged"), from_remote="team24.example")
print("forged 'from' over s2s dropped:", "forged" not in bodies(race.inbox[steward]))
print("s2s hops:", net.s2s_log)

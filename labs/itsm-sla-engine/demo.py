from datetime import datetime

from sla import Ticket

fri_4pm = datetime(2026, 10, 2, 16, 0)       # a Friday
mon_10am = datetime(2026, 10, 5, 10, 0)
cases = [
    ("Timing system down at the track (impact 1, urgency 1)", Ticket(fri_4pm, 1, 1)),
    ("Dashboard slow for one team (impact 2, urgency 2)", Ticket(fri_4pm, 2, 2)),
    ("Same, but waiting on the customer all weekend", Ticket(fri_4pm, 2, 2, [(datetime(2026, 10, 2, 17, 0), "awaiting customer"),
                                                                            (datetime(2026, 10, 5, 9, 0), "in progress")])),
]
print(f"Checked at {mon_10am:%a %d %b %H:%M}, tickets opened {fri_4pm:%a %H:%M}")
for label, t in cases:
    s, pct = t.status(mon_10am)
    print(f"  {t.priority} {label:56} SLA used {t.elapsed(mon_10am)} ({pct:.0%}) -> {s}")

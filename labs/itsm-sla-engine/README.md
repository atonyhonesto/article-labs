<sub>[← all labs](../../README.md)</sub>

# An ITSM priority and SLA engine

> Priority comes from impact and urgency. The clock depends on the priority, the calendar and who you're waiting on.

`Python` · `stdlib`

**Companion to:**
- [ITSM Platforms Are More Strategic Than Ever](https://www.linkedin.com/pulse/itsm-platforms-more-strategic-than-ever-tony-honesto-j8msc/)
- [IFS assyst - Enterprise Service Delivery](https://www.linkedin.com/pulse/ifs-assyst-enterprise-service-delivery-tony-honesto-sncfc/)

## What it shows

- ITIL priority matrix: impact × urgency → P1–P5.
- P1 clocks run 24×7; lower priorities only count business hours (Mon–Fri, 08:00–18:00).
- The clock pauses while the ticket is waiting on the customer.
- Each ticket reports SLA used and OK / AT RISK / BREACHED.

## Run it

```bash
bash labs/itsm-sla-engine/ci.sh        # install, test, run the demo
# or, from this folder:
python demo.py
```

Real output:

```text
Checked at Mon 05 Oct 10:00, tickets opened Fri 16:00
  P1 Timing system down at the track (impact 1, urgency 1)    SLA used 2 days, 18:00:00 (1650%) -> BREACHED
  P3 Dashboard slow for one team (impact 2, urgency 2)        SLA used 4:00:00 (17%) -> OK
  P3 Same, but waiting on the customer all weekend            SLA used 2:00:00 (8%) -> OK
```

## What's in here

| File | Purpose |
|---|---|
| `sla.py` | Priority matrix, business-hours clock and ticket status |
| `demo.py` | Three tickets opened on a Friday afternoon, checked on Monday |
| `tests/` | Matrix, calendar and pause tests |

## Simulated here vs. a real deployment

| In this lab | In production |
|---|---|
| Hard-coded calendar | Holiday calendars and per-customer service hours |
| Python objects | ServiceNow / IFS assyst / Jira Service Management SLA definitions |
| Status string | Escalation workflows and notifications at 75% and 100% |

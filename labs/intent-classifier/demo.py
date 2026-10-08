from intents import build, parse

model = build()
for text in ("hey can u get us a table for 4 at 8:30", "is the spa open tmrw", "late checkout? like 1pm",
             "what's the wifi password and also my card was charged twice"):
    p = parse(model, text)
    route = "-> HUMAN" if p.handoff else f"-> {p.intent}"
    print(f"{text!r:62} {route:16} conf {p.confidence:.2f} slots {p.slots}")

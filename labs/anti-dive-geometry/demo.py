from antidive import Wishbone, anti_dive_percent, pitch_change_deg

car = dict(wheelbase=3.6, cg_height=0.28, front_brake_share=0.58)
setups = {
    "parallel wishbones": (Wishbone((-0.45, 0.42), (0.0, 0.42)), Wishbone((-0.45, 0.14), (0.0, 0.14))),
    "mild anti-dive":     (Wishbone((-0.45, 0.39), (0.0, 0.42)), Wishbone((-0.45, 0.14), (0.0, 0.14))),
    "strong anti-dive":   (Wishbone((-0.45, 0.36), (0.0, 0.42)), Wishbone((-0.45, 0.15), (0.0, 0.14))),
}
for name, (up, lo) in setups.items():
    pct = anti_dive_percent(up, lo, **car)
    pitch = pitch_change_deg(5.0, 800, car["cg_height"], car["wheelbase"], 350_000, pct)
    print(f"{name:19}: anti-dive {pct:5.1f}%  nose-down pitch at 5 g braking {pitch:.2f}°")

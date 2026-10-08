import os
import tempfile

import numpy as np

from laptime_net import Trained, make_data, train

x, y = make_data()
t = train(x, y)
print(f"Trained on {int(0.8 * len(x))} laps, stopped after {t.epochs_run} epochs, "
      f"validation MAE {t.val_mae_s * 1000:.0f} ms")
probe = np.array([[5, 80, 35, 1], [25, 30, 35, 1], [25, 30, 35, 0]], dtype=np.float32)
for row, pred in zip(probe, t.predict(probe)):
    print(f"  age {row[0]:>2.0f}, fuel {row[1]:>3.0f} kg, {'soft' if row[3] else 'hard'}: {pred:.2f} s")
with tempfile.TemporaryDirectory() as d:
    path = os.path.join(d, "laptime.pt")
    t.save(path)
    same = np.allclose(Trained.load(path).predict(probe), t.predict(probe))
    print(f"Checkpoint round-trip identical: {same}")

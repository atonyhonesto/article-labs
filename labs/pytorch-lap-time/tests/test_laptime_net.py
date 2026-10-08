import os
import tempfile
import unittest

import numpy as np

from laptime_net import Trained, make_data, train


class LapTimeNetTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        x, y = make_data(n=2000)
        cls.t = train(x, y, epochs=150)

    def test_beats_predicting_the_mean(self):
        x, y = make_data(n=500, seed=9)
        baseline = np.abs(y - y.mean()).mean()
        self.assertLess(np.abs(self.t.predict(x) - y).mean(), 0.5 * baseline)

    def test_learns_the_soft_tire_cliff(self):
        fresh, old = self.t.predict(np.array([[5, 50, 35, 1], [30, 50, 35, 1]], dtype=np.float32))
        self.assertGreater(old - fresh, 1.0)

    def test_checkpoint_round_trip(self):
        probe = np.array([[10, 40, 30, 0]], dtype=np.float32)
        with tempfile.TemporaryDirectory() as d:
            p = os.path.join(d, "m.pt")
            self.t.save(p)
            np.testing.assert_allclose(Trained.load(p).predict(probe), self.t.predict(probe), rtol=1e-6)


if __name__ == "__main__":
    unittest.main()

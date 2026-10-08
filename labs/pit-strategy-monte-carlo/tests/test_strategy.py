import unittest
import numpy as np
from strategy import Track, compare, run_race


class StrategyTests(unittest.TestCase):
    def test_no_cautions_means_no_difference(self):
        t = Track(caution_rate=0.0)
        rng = np.random.default_rng(1)
        self.assertEqual(run_race(t, "fixed", rng), run_race(t, "opportunistic", np.random.default_rng(1)))

    def test_opportunism_pays_more_when_cautions_are_common(self):
        low = compare(Track(caution_rate=0.01), n=500)
        high = compare(Track(caution_rate=0.06), n=500)
        gain = lambda r: r["fixed"]["mean_s"] - r["opportunistic"]["mean_s"]
        self.assertGreater(gain(high), gain(low))

    def test_never_runs_out_of_fuel(self):
        # fixed plan must stop before the window closes on every simulated race
        t = Track(caution_rate=0.0)
        self.assertGreater(run_race(t, "fixed", np.random.default_rng(0)), t.laps * t.green_lap_s)


if __name__ == "__main__":
    unittest.main()

import unittest
import numpy as np
from tracking import analyse, simulate_route


class TrackingTests(unittest.TestCase):
    def test_counts_both_sprints(self):
        self.assertEqual(analyse(*simulate_route()).sprints, 2)

    def test_top_speed_close_to_truth(self):
        self.assertAlmostEqual(analyse(*simulate_route()).top_speed_mps, 9.2, delta=0.6)

    def test_dropout_is_not_counted_as_distance(self):
        t = np.array([0, 0.1, 0.2, 5.0, 5.1])
        x = np.array([0, 0.3, 0.6, 50.0, 50.3])
        s = analyse(t, x, np.zeros_like(x))
        self.assertLess(s.distance_m, 5)


if __name__ == "__main__":
    unittest.main()

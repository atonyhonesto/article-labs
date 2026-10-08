import unittest
from quartercar import Car, bump, rough_road, simulate, sweep


class QuarterCarTests(unittest.TestCase):
    def test_body_mode_is_in_the_passenger_car_range(self):
        self.assertTrue(1.0 < Car().body_hz < 2.0)

    def test_flat_road_is_still(self):
        r = simulate(Car(), lambda t: 0.0 * t, t_end=0.5)
        self.assertAlmostEqual(r["comfort_rms_ms2"], 0.0, places=6)

    def test_more_damping_less_travel(self):
        travel = [r["travel_mm"] for _, _, r in sweep(Car(), bump(), ratios=(0.1, 0.3, 1.0))]
        self.assertGreater(travel[0], travel[1])
        self.assertGreater(travel[1], travel[2])

    def test_tradeoff_exists_on_rough_road(self):
        res = {z: r for z, _, r in sweep(Car(), rough_road(), ratios=(0.1, 0.3, 1.0), t_end=4.0)}
        self.assertLess(res[0.3]["grip_rms_pct"], res[0.1]["grip_rms_pct"])      # too soft: wheel hop
        self.assertLess(res[0.3]["comfort_rms_ms2"], res[1.0]["comfort_rms_ms2"])  # too stiff: harsh


if __name__ == "__main__":
    unittest.main()

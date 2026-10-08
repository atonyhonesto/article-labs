import unittest
from pace import driver_pace, representative_laps, stint_degradation, synthetic_session


class PaceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.laps = synthetic_session()

    def test_pit_and_safety_car_laps_removed(self):
        rep = representative_laps(self.laps)
        self.assertFalse(rep.PitInTime.any() or rep.PitOutTime.any())
        self.assertTrue((rep.TrackStatus == "1").all())

    def test_driver_order_recovers_true_pace(self):
        self.assertEqual(list(driver_pace(self.laps).index), ["AAA", "BBB", "CCC"])

    def test_degradation_estimate_close_to_truth(self):
        self.assertAlmostEqual(stint_degradation(self.laps).deg_s_per_lap.median(), 0.06, delta=0.02)


if __name__ == "__main__":
    unittest.main()

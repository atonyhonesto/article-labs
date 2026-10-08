import unittest
from pitwindow import best_pit_lap, fit_degradation, race_time, simulate_stints


class PitWindowTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.model = fit_degradation(simulate_stints())

    def test_model_learns_degradation(self):
        import pandas as pd
        fresh = self.model.predict(pd.DataFrame({"tire_age": [0], "track_temp": [35], "fuel_kg": [50]}))[0]
        worn = self.model.predict(pd.DataFrame({"tire_age": [25], "track_temp": [35], "fuel_kg": [50]}))[0]
        self.assertGreater(worn - fresh, 1.0)

    def test_optimum_is_inside_window_and_not_an_edge(self):
        lap, _, times = best_pit_lap(self.model, 50, 35, (15, 35))
        self.assertTrue(15 < lap < 35)
        self.assertEqual(times[lap], min(times.values()))

    def test_hotter_track_does_not_pit_later(self):
        cool, _, _ = best_pit_lap(self.model, 50, 26, (15, 35))
        hot, _, _ = best_pit_lap(self.model, 50, 44, (15, 35))
        self.assertLessEqual(abs(hot - 25), abs(cool - 25) + 3)

    def test_race_time_includes_pit_loss(self):
        with_loss = race_time(self.model, 50, 25, 35, pit_loss_s=21)
        without = race_time(self.model, 50, 25, 35, pit_loss_s=0)
        self.assertAlmostEqual(with_loss - without, 21, places=6)


if __name__ == "__main__":
    unittest.main()

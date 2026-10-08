import math
import unittest
import analysis


class AnalysisTests(unittest.TestCase):
    def test_distance_close_to_mean_speed_times_time(self):
        self.assertAlmostEqual(analysis.results["distance_m"], 600, delta=1)

    def test_dominant_frequency(self):
        self.assertAlmostEqual(analysis.results["dominant_hz"], 12.5, places=6)

    def test_time_constant_recovered(self):
        self.assertAlmostEqual(analysis.results["tau_s"], 3.2, delta=0.1)

    def test_matlab_file_mirrors_python(self):
        m = (analysis.__file__.replace(".py", ".m"))
        text = open(m).read()
        for fn in ("trapz", "fft", "polyfit"):
            self.assertIn(fn, text)
        self.assertTrue(math.isfinite(analysis.results["mean_speed"]))


if __name__ == "__main__":
    unittest.main()

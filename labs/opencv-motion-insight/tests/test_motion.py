import unittest
from motion import MotionDetector, speed_px_per_frame, synthetic_frames


class MotionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.det = MotionDetector()
        cls.found = []
        for i, f in enumerate(synthetic_frames()):
            cls.found += cls.det.process(i, f)

    def test_static_noise_is_ignored(self):
        self.assertFalse([d for d in self.found if 10 <= d.frame < 30])

    def test_object_detected_promptly(self):
        self.assertLessEqual(min(d.frame for d in self.found), 32)

    def test_speed_estimate(self):
        self.assertAlmostEqual(speed_px_per_frame([d for d in self.found if d.frame > 35]), 6.0, delta=1.0)


if __name__ == "__main__":
    unittest.main()

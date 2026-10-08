import unittest
import numpy as np
from offside import LANDMARKS_M, camera_homography, estimate_homography, offside_decision, offside_line_px, project


class OffsideTests(unittest.TestCase):
    def setUp(self):
        self.truth = camera_homography()
        self.H = estimate_homography(LANDMARKS_M, project(self.truth, LANDMARKS_M))

    def test_homography_round_trips_pitch_points(self):
        pts = np.array([[20.0, 10.0], [40.0, 60.0]])
        back = project(self.H, project(self.truth, pts))
        np.testing.assert_allclose(back, pts, atol=1e-6)

    def test_decision_in_pitch_space(self):
        d = project(self.truth, np.array([[15.0, 30.0]]))[0]
        a_on = project(self.truth, np.array([[15.5, 50.0]]))[0]
        a_off = project(self.truth, np.array([[14.5, 10.0]]))[0]
        self.assertFalse(offside_decision(self.H, a_on, d)[0])
        self.assertTrue(offside_decision(self.H, a_off, d)[0])

    def test_line_is_slanted_in_the_image(self):
        d = project(self.truth, np.array([[15.0, 30.0]]))[0]
        a, b = offside_line_px(self.H, d)
        self.assertGreater(abs(a[0] - b[0]), 20)

    def test_ransac_survives_one_bad_click(self):
        clicks = project(self.truth, LANDMARKS_M)
        clicks[2] += [80, -60]
        H = estimate_homography(LANDMARKS_M, clicks)
        np.testing.assert_allclose(project(H, project(self.truth, np.array([[30.0, 30.0]]))), [[30, 30]], atol=0.3)


if __name__ == "__main__":
    unittest.main()

import unittest
import numpy as np
from twin import CellParams, Twin, drive_cycle, monitor, ocv


class TwinTests(unittest.TestCase):
    def test_ocv_rises_with_soc(self):
        self.assertTrue(all(ocv(a) < ocv(b) for a, b in zip(np.linspace(0, 0.9, 10), np.linspace(0.1, 1, 10))))

    def test_coulomb_counting(self):
        t = Twin(CellParams(capacity_ah=5.0), soc=1.0)
        for _ in range(3600):
            t.step(5.0, 1.0)              # 1C for an hour
        self.assertAlmostEqual(t.soc, 0.0, places=6)

    def test_load_heats_the_cell(self):
        t = Twin(CellParams())
        for _ in range(600):
            t.step(20.0, 1.0)
        self.assertGreater(t.temp_c, 30)

    def test_twin_flags_aged_cell_only(self):
        cur = drive_cycle(900)
        twin, healthy, aged = Twin(CellParams()), Twin(CellParams()), Twin(CellParams(r0_ohm=0.024, r1_ohm=0.016))
        p = np.array([twin.step(i, 1) for i in cur])
        self.assertIsNone(monitor(np.array([healthy.step(i, 1) for i in cur]), p))
        self.assertIsNotNone(monitor(np.array([aged.step(i, 1) for i in cur]), p))


if __name__ == "__main__":
    unittest.main()

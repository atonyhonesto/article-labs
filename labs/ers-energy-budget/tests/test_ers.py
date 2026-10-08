import unittest
from ers import PowerUnit, simulate_lap, sustainable_deploy_fraction


class ErsTests(unittest.TestCase):
    def test_soc_never_exceeds_battery(self):
        pu = PowerUnit(350, 0)
        _, soc = simulate_lap(pu, 4.0, deploy_fraction=0.0)
        self.assertLessEqual(soc, pu.battery_mj)

    def test_mguh_raises_sustainable_deployment(self):
        self.assertGreater(sustainable_deploy_fraction(PowerUnit(120, 60)),
                           sustainable_deploy_fraction(PowerUnit(120, 0)))

    def test_full_deploy_without_mguh_drains(self):
        pu = PowerUnit(350, 0)
        soc = pu.battery_mj
        for _ in range(5):
            _, soc = simulate_lap(pu, soc, 1.0)
        self.assertLess(soc, 1.0)


if __name__ == "__main__":
    unittest.main()

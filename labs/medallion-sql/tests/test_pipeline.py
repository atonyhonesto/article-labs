import unittest
from pipeline import connect, run_batch


def lap(car, n, t, at):
    return {"race_id": "R", "car": car, "lap": n, "lap_time_s": t, "recorded_at": at}


class MedallionTests(unittest.TestCase):
    def test_latest_record_wins(self):
        con = connect()
        run_batch(con, "a", [lap("1", 1, 40.0, "2026-01-01T00:00"), lap("1", 1, 39.0, "2026-01-01T00:05")])
        self.assertEqual(con.execute("SELECT lap_time_s FROM silver_laps").fetchone()[0], 39.0)

    def test_older_correction_does_not_overwrite_newer(self):
        con = connect()
        run_batch(con, "a", [lap("1", 1, 39.0, "2026-01-01T00:05")])
        run_batch(con, "b", [lap("1", 1, 45.0, "2026-01-01T00:01")])
        self.assertEqual(con.execute("SELECT lap_time_s FROM silver_laps").fetchone()[0], 39.0)

    def test_quality_rules_and_rejects(self):
        con = connect()
        counts = run_batch(con, "a", [lap("1", 1, 39.0, "t"), lap("", 1, 39.0, "t"), lap("2", 1, 5.0, "t")])
        self.assertEqual((counts["silver_laps"], counts["dq_rejects"]), (1, 2))

    def test_replay_is_idempotent_in_silver_and_gold(self):
        con = connect()
        rows = [lap("1", n, 40 + n, f"t{n}") for n in range(1, 4)]
        first = run_batch(con, "a", rows)
        again = run_batch(con, "a2", rows)
        self.assertEqual((first["silver_laps"], first["gold_car_summary"]), (again["silver_laps"], again["gold_car_summary"]))


if __name__ == "__main__":
    unittest.main()

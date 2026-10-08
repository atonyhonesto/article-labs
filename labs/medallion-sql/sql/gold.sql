-- Gold: business-ready aggregates, rebuilt from silver so they are always consistent.
DELETE FROM gold_car_summary;
INSERT INTO gold_car_summary (race_id, car, laps, best_lap_s, avg_lap_s, lap_time_variance)
SELECT
    race_id,
    car,
    COUNT(*)                                         AS laps,
    MIN(lap_time_s)                                  AS best_lap_s,
    ROUND(AVG(lap_time_s), 3)                        AS avg_lap_s,
    ROUND(AVG(lap_time_s * lap_time_s) - AVG(lap_time_s) * AVG(lap_time_s), 4) AS lap_time_variance
FROM silver_laps
GROUP BY race_id, car;

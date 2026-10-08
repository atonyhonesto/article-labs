-- Silver: typed, deduplicated, validated. Only the latest version of each lap survives.
INSERT INTO silver_laps (race_id, car, lap, lap_time_s, recorded_at)
SELECT race_id, car, lap, lap_time_s, recorded_at
FROM (
    SELECT
        TRIM(json_extract(payload, '$.race_id'))                       AS race_id,
        TRIM(json_extract(payload, '$.car'))                           AS car,
        CAST(json_extract(payload, '$.lap') AS INTEGER)                AS lap,
        CAST(json_extract(payload, '$.lap_time_s') AS REAL)            AS lap_time_s,
        json_extract(payload, '$.recorded_at')                         AS recorded_at,
        ROW_NUMBER() OVER (
            PARTITION BY json_extract(payload, '$.race_id'), json_extract(payload, '$.car'), json_extract(payload, '$.lap')
            ORDER BY json_extract(payload, '$.recorded_at') DESC
        ) AS rn
    FROM bronze_events
    WHERE batch_id = :batch_id
) AS ranked
WHERE rn = 1
  AND lap_time_s BETWEEN 20 AND 300          -- quality rule: plausible lap times only
  AND car IS NOT NULL AND car <> ''
ON CONFLICT (race_id, car, lap) DO UPDATE SET
    lap_time_s  = excluded.lap_time_s,
    recorded_at = excluded.recorded_at
WHERE excluded.recorded_at > silver_laps.recorded_at;

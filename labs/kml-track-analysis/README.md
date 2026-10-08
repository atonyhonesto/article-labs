<sub>[← all labs](../../README.md)</sub>

# KML track analysis: distance, speed and sectors

> A KML file is just XML with coordinates. Add timestamps and a bit of trigonometry and it becomes a lap.

`Python` · `stdlib`

**Companion to:**
- [KML Data Into Actionable Geospatial Insights](https://www.linkedin.com/pulse/kml-data-actionable-geospatial-insights-tony-honesto-bf14c/)

## What it shows

- Parsing a `gx:Track` (timestamps plus coordinates) and named sector placemarks with the standard library.
- Great-circle distance with the haversine formula.
- Average and top speed, and timed sectors split at the nearest track point to each marker.

## Run it

```bash
bash labs/kml-track-analysis/ci.sh        # install, test, run the demo
# or, from this folder:
python demo.py
```

Real output:

```text
121 track points, sector markers ['S1', 'S2']
Lap distance 2819 m (1.75 mi), lap time 42.35 s, average 148.9 mph, top 167.8 mph
Sector times: S1 15.02 s | S2 12.36 s | S3 14.97 s
```

## What's in here

| File | Purpose |
|---|---|
| `kml.py` | KML parser, haversine and lap analysis |
| `lap.kml` | A generated oval lap with two sector markers |
| `demo.py` | Prints distance, speeds and sector times |
| `tests/` | Haversine and sector tests |

## Simulated here vs. a real deployment

| In this lab | In production |
|---|---|
| Generated KML | Exports from GPS loggers, Google Earth or telematics platforms |
| Nearest-point sectors | Line-crossing detection with interpolation between samples |
| Plain Python | GeoPandas / Shapely for larger data sets and spatial joins |

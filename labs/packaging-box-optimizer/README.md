<sub>[← all labs](../../README.md)</sub>

# Right-sized boxes vs. a carton catalog

> Shipping air is expensive. Cut the box to the order and the savings show up in four places.

`Python`

**Companion to:**
- [AI-Enhanced On-Demand Packaging with Packsize](https://www.linkedin.com/pulse/ai-enhanced-on-demand-packaging-packsize-tony-honesto-d6qmc/)

## What it shows

- A stacking heuristic for the order's bounding box, with clearance for protection.
- Smallest catalog carton that fits (any orientation) vs. a box cut to fit.
- Corrugate area, void fill, dimensional weight (cubic inches / 139) and trailer cube for a day of orders.

## Run it

```bash
bash labs/packaging-box-optimizer/ci.sh        # install, test, run the demo
# or, from this folder:
python demo.py
```

Real output:

```text
One order: a book and a phone case
  catalog  box 12x10x8   board  712 in²  void  734 in³  billed 7 lb
  custom   box 12x8x6    board  528 in²  void  350 in³  billed 5 lb

A day of 500 orders: catalog cartons -> boxes cut to fit
  corrugate      2,785 ft² ->   1,662 ft²   (40% less)
  void fill      293.9 ft³ ->    87.6 ft³   (70% less)
  billed wt      4,764 lb  ->   2,500 lb    (48% less)
  parcel cube    357.8 ft³ ->   151.5 ft³   (58% less trailer space)
```

## What's in here

| File | Purpose |
|---|---|
| `boxes.py` | Fit, box sizing, board area and dimensional weight |
| `demo.py` | One order, then a day of 500 |
| `tests/` | Fit, billing and savings tests |

## Simulated here vs. a real deployment

| In this lab | In production |
|---|---|
| Stacking heuristic | 3D bin-packing with fragility and orientation rules |
| Seven catalog sizes | A site's actual carton catalog and machine limits |
| One divisor | Carrier-specific dimensional rules and rate tables |

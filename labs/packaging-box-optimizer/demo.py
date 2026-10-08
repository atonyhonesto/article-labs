from boxes import Item, compare, orders, summarise

one = [Item(11, 7, 2, 1.2), Item(6, 4, 3, 0.8)]
r = compare(one)
print("One order: a book and a phone case")
for k in ("catalog", "custom"):
    b = r[k]
    print(f"  {k:<8} box {'x'.join(str(int(d)) for d in b['box']):<9} board {b['board']:>4.0f} in²  "
          f"void {b['void']:>4.0f} in³  billed {b['billable_lb']} lb")

day = orders()
t = summarise(day)
cat, cus = t["catalog"], t["custom"]
pct = lambda a, b: (a - b) / a * 100
extra = f" ({t['oversize']} too big for the catalog left out)" if t["oversize"] else ""
print(f"\nA day of {len(day)} orders{extra}: catalog cartons -> boxes cut to fit")
print(f"  corrugate    {cat['board'] / 144:>7,.0f} ft² -> {cus['board'] / 144:>7,.0f} ft²   ({pct(cat['board'], cus['board']):.0f}% less)")
print(f"  void fill    {cat['void'] / 1728:>7,.1f} ft³ -> {cus['void'] / 1728:>7,.1f} ft³   ({pct(cat['void'], cus['void']):.0f}% less)")
print(f"  billed wt    {cat['billable_lb']:>7,} lb  -> {cus['billable_lb']:>7,} lb    ({pct(cat['billable_lb'], cus['billable_lb']):.0f}% less)")
print(f"  parcel cube  {cat['volume'] / 1728:>7,.1f} ft³ -> {cus['volume'] / 1728:>7,.1f} ft³   ({pct(cat['volume'], cus['volume']):.0f}% less trailer space)")

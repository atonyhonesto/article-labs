import unittest
from boxes import Item, billable, catalog_box, custom_box, fits, pack_dims, summarise, orders


class BoxTests(unittest.TestCase):
    def test_fits_any_orientation(self):
        self.assertFalse(fits((10, 2, 6), (6, 10, 1.5)))
        self.assertTrue(fits((10, 2, 6), (6, 10, 8)))

    def test_custom_box_never_bigger_than_catalog(self):
        for order in orders(100):
            inner = pack_dims(order)
            cat = catalog_box(inner)
            if cat:
                c = custom_box(inner)
                self.assertLessEqual(c[0] * c[1] * c[2], cat[0] * cat[1] * cat[2])

    def test_dim_weight_beats_light_items(self):
        self.assertEqual(billable((18, 14, 12), 2.0), 22)    # 3024 / 139 = 21.8 -> 22 lb
        self.assertEqual(billable((8, 6, 4), 5.0), 5)

    def test_items_stack(self):
        self.assertEqual(pack_dims([Item(10, 8, 2, 1), Item(6, 4, 3, 1)]), (10, 8, 5))

    def test_day_saves_material(self):
        t = summarise(orders(200))
        self.assertLess(t["custom"]["board"], t["catalog"]["board"])
        self.assertLess(t["custom"]["billable_lb"], t["catalog"]["billable_lb"])


if __name__ == "__main__":
    unittest.main()

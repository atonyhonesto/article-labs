import unittest
import pandas as pd
from pipeline import CATEGORICAL, NUMERIC, build, cross_validated_auc, prospects


class PipelineTests(unittest.TestCase):
    def test_auc_well_above_chance(self):
        self.assertGreater(cross_validated_auc(prospects(n=600)), 0.75)

    def test_scores_unseen_category_and_missing_values(self):
        df = prospects(n=300)
        model = build().fit(df[NUMERIC + CATEGORICAL], df.made_roster)
        row = df[NUMERIC + CATEGORICAL].head(1).copy()
        row["position"] = "K"            # never seen in training
        row["vertical_in"] = None
        p = model.predict_proba(row)[0, 1]
        self.assertTrue(0 <= p <= 1)


if __name__ == "__main__":
    unittest.main()

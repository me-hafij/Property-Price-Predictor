import unittest
from main import load_dataset, estimate_price_lakh, predict_price, format_price

class PredictorTests(unittest.TestCase):
    def test_dataset_has_records(self):
        self.assertGreaterEqual(len(load_dataset()), 20)

    def test_estimate_is_positive(self):
        p = dict(area_sqft=1000, bedrooms=2, bathrooms=2, age_years=4,
                 floor=2, parking=1, location="Kolkata")
        self.assertGreater(estimate_price_lakh(p), 0)

    def test_invalid_area_rejected(self):
        p = dict(area_sqft=0, bedrooms=2, bathrooms=2, age_years=4,
                 floor=2, parking=1, location="Kolkata")
        with self.assertRaises(ValueError):
            estimate_price_lakh(p)

    def test_format_lakh(self):
        self.assertIn("lakh", format_price(45.5))

    def test_format_crore(self):
        self.assertIn("crore", format_price(125))

    def test_prediction_fallback(self):
        p = dict(area_sqft=1000, bedrooms=2, bathrooms=2, age_years=4,
                 floor=2, parking=1, location="Kolkata")
        value, method = predict_price(p, None)
        self.assertGreater(value, 0)
        self.assertTrue(method)

if __name__ == "__main__":
    unittest.main()

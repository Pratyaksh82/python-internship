"""
AUTOMATED TEST SUITE FOR WEEK 3 DATA ENGINE
Covers unit tests, edge cases, error conditions, and an end-to-end integration test.
Uses standard library unittest for fast, deterministic execution.
"""

import unittest
from week3_testing.engine import (
    DataPipeline,
    MetricsCalculator,
    TextCleaner,
    ValidationError
)


class TestTextCleaner(unittest.TestCase):
    """Unit tests for string sanitization and PII masking."""

    def test_sanitize_whitespace(self):
        raw = "   John    Doe   \n\t  "
        self.assertEqual(TextCleaner.sanitize_whitespace(raw), "John Doe")

    def test_slugify(self):
        text = "Python Automated Testing 2026!"
        self.assertEqual(TextCleaner.slugify(text), "python-automated-testing-2026")

    def test_mask_email_valid(self):
        email = "pratyaksh@example.com"
        masked = TextCleaner.mask_email(email)
        self.assertTrue(masked.startswith("p") and masked.endswith("@example.com"))
        self.assertIn("*", masked)

    def test_mask_email_invalid_format_raises_error(self):
        with self.assertRaises(ValueError):
            TextCleaner.mask_email("invalid-email-address")


class TestMetricsCalculator(unittest.TestCase):
    """Unit tests for statistical calculations and edge cases."""

    def test_compute_mean_and_empty_guard(self):
        self.assertEqual(MetricsCalculator.compute_mean([10.0, 20.0, 30.0]), 20.0)
        with self.assertRaises(ValueError):
            MetricsCalculator.compute_mean([])

    def test_compute_median_odd_and_even(self):
        self.assertEqual(MetricsCalculator.compute_median([1, 5, 2]), 2.0)
        self.assertEqual(MetricsCalculator.compute_median([1, 2, 3, 4]), 2.5)

    def test_compute_stdev(self):
        data = [10.0, 12.0, 23.0, 23.0, 16.0, 23.0, 21.0, 16.0]
        stdev = MetricsCalculator.compute_stdev(data)
        self.assertAlmostEqual(stdev, 5.2372, places=3)
        with self.assertRaises(ValueError):
            MetricsCalculator.compute_stdev([5.0])

    def test_detect_iqr_outliers(self):
        data = [10, 12, 12, 13, 12, 11, 14, 100]  # 100 is an extreme outlier
        outliers, bounds = MetricsCalculator.detect_iqr_outliers(data)
        self.assertIn(100, outliers)


class TestDataPipelineIntegration(unittest.TestCase):
    """Integration test suite verifying end-to-end data pipeline."""

    def setUp(self):
        self.pipeline = DataPipeline()

    def test_validation_rejects_missing_field(self):
        bad_record = {"id": 1, "name": "Alice", "amount": 50.0}  # missing email
        with self.assertRaises(ValidationError):
            self.pipeline.validate_record(bad_record)

    def test_validation_rejects_negative_amount(self):
        bad_record = {"id": 1, "name": "Alice", "email": "a@test.com", "amount": -10.0}
        with self.assertRaises(ValidationError):
            self.pipeline.validate_record(bad_record)

    def test_end_to_end_pipeline_processing(self):
        records = [
            {"id": 1, "name": "  Alice   Smith ", "email": "alice@company.com", "amount": 100.0},
            {"id": 2, "name": "Bob   Jones", "email": "bob@org.net", "amount": 200.0},
            {"id": 3, "name": "Corrupt Record", "email": "corrupt", "amount": -5.0}  # should be rejected
        ]
        summary = self.pipeline.process_records(records)

        self.assertEqual(summary["total_processed"], 3)
        self.assertEqual(summary["valid_count"], 2)
        self.assertEqual(summary["rejected_count"], 1)
        self.assertEqual(summary["total_revenue"], 300.0)
        self.assertEqual(summary["average_revenue"], 150.0)
        self.assertEqual(summary["records"][0]["name"], "Alice Smith")
        self.assertTrue(summary["records"][0]["email"].startswith("a*"))


if __name__ == "__main__":
    unittest.main()

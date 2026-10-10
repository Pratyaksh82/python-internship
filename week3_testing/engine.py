"""
WEEK 3: Moderately Complex Data Processing, Sanitization & Analytics Engine
Engineered for Test-Driven Development (TDD), modularity, and high testability.

Components:
1. TextCleaner: String sanitization, slugification, and PII masking.
2. MetricsCalculator: Statistical computations (mean, median, stdev, outlier bounds).
3. DataPipeline: Structured dictionary record validation and transformation pipeline.
"""

import math
import re
from typing import Any, Dict, List, Optional, Tuple


class ValidationError(Exception):
    """Raised when record fails schema validation."""
    pass


class TextCleaner:
    """Provides resilient string sanitization and PII masking."""

    @staticmethod
    def sanitize_whitespace(text: str) -> str:
        """Trims leading/trailing whitespace and collapses repeated spaces."""
        if not isinstance(text, str):
            raise TypeError("Input text must be a string.")
        return re.sub(r"\s+", " ", text).strip()

    @staticmethod
    def slugify(text: str) -> str:
        """Converts text to URL-friendly lowercase slug."""
        if not isinstance(text, str):
            raise TypeError("Input text must be a string.")
        cleaned = re.sub(r"[^\w\s-]", "", text.lower()).strip()
        return re.sub(r"[-\s]+", "-", cleaned)

    @staticmethod
    def mask_email(email: str) -> str:
        """Masks username part of email for privacy (e.g. j***e@domain.com)."""
        if not isinstance(email, str) or "@" not in email:
            raise ValueError(f"Invalid email format: '{email}'")
        user, domain = email.strip().split("@", 1)
        if len(user) <= 2:
            masked_user = user[0] + "*"
        else:
            masked_user = user[0] + ("*" * (len(user) - 2)) + user[-1]
        return f"{masked_user}@{domain.lower()}"


class MetricsCalculator:
    """Provides statistical aggregations and outlier boundaries."""

    @staticmethod
    def compute_mean(numbers: List[float]) -> float:
        """Calculates arithmetic mean; raises ValueError on empty list."""
        if not numbers:
            raise ValueError("Cannot compute mean of an empty sequence.")
        return sum(numbers) / len(numbers)

    @staticmethod
    def compute_median(numbers: List[float]) -> float:
        """Calculates median of numeric sequence."""
        if not numbers:
            raise ValueError("Cannot compute median of an empty sequence.")
        s = sorted(numbers)
        n = len(s)
        mid = n // 2
        if n % 2 == 1:
            return float(s[mid])
        return (s[mid - 1] + s[mid]) / 2.0

    @staticmethod
    def compute_stdev(numbers: List[float]) -> float:
        """Calculates sample standard deviation (n-1 degrees of freedom)."""
        if len(numbers) < 2:
            raise ValueError("Standard deviation requires at least 2 observations.")
        mean = sum(numbers) / len(numbers)
        variance = sum((x - mean) ** 2 for x in numbers) / (len(numbers) - 1)
        return math.sqrt(variance)

    @staticmethod
    def detect_iqr_outliers(numbers: List[float]) -> Tuple[List[float], Tuple[float, float]]:
        """Identifies outliers using the Interquartile Range (IQR) technique."""
        if len(numbers) < 4:
            return [], (float("-inf"), float("inf"))
        s = sorted(numbers)
        n = len(s)
        q1 = s[n // 4]
        q3 = s[(3 * n) // 4]
        iqr = q3 - q1
        lower_bound = q1 - (1.5 * iqr)
        upper_bound = q3 + (1.5 * iqr)
        outliers = [x for x in s if x < lower_bound or x > upper_bound]
        return outliers, (lower_bound, upper_bound)


class DataPipeline:
    """Validates, cleans, and aggregates batches of customer records."""

    def __init__(self, required_fields: Optional[List[str]] = None):
        self.required_fields = required_fields or ["id", "name", "email", "amount"]

    def validate_record(self, record: Dict[str, Any]) -> bool:
        """Ensures all required fields exist and values are non-empty."""
        for field in self.required_fields:
            if field not in record or record[field] is None or record[field] == "":
                raise ValidationError(f"Missing or empty required field: '{field}'")
        if not isinstance(record["amount"], (int, float)) or record["amount"] < 0:
            raise ValidationError(f"Field 'amount' must be a non-negative number, got {record['amount']}")
        return True

    def process_records(self, records: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Cleans, masks, and computes summary metrics across valid records."""
        valid_records = []
        rejected_count = 0
        amounts = []

        for r in records:
            try:
                self.validate_record(r)
                cleaned = dict(r)
                cleaned["name"] = TextCleaner.sanitize_whitespace(r["name"])
                cleaned["email"] = TextCleaner.mask_email(r["email"])
                valid_records.append(cleaned)
                amounts.append(float(r["amount"]))
            except (ValidationError, ValueError):
                rejected_count += 1

        summary = {
            "total_processed": len(records),
            "valid_count": len(valid_records),
            "rejected_count": rejected_count,
            "total_revenue": sum(amounts),
            "average_revenue": MetricsCalculator.compute_mean(amounts) if amounts else 0.0,
            "records": valid_records
        }
        return summary

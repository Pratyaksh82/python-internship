# Test Documentation and TDD Methodology (Week 3)

**Program:** Junior Python Developer Virtual Internship (Yuva Learn)  
**Milestone:** Week 3: Writing Automated Tests for Python Applications  
**Author:** Pratyaksh ([@Pratyaksh82](https://github.com/Pratyaksh82))  

---

## 1. Test-Driven Development (TDD) Methodology
The project follows the standard **Red-Green-Refactor** TDD lifecycle:
1. **Red (Write Failing Tests First):** Define unit tests capturing requirements, expected outputs, type constraints, and boundary edge cases (e.g. empty lists, negative amounts, invalid emails).
2. **Green (Write Minimum Functional Code):** Implement the simplest logic in `TextCleaner`, `MetricsCalculator`, and `DataPipeline` to turn all tests green.
3. **Refactor (Optimize and Clean):** Clean up string sanitization regexes, streamline sample variance calculation, and ensure defensive exception raising (`ValidationError`, `ValueError`, `TypeError`).

---

## 2. Test Case Specification Matrix

| Test Method | Target Class / Function | Test Type | Input Condition | Expected Behavior / Invariant |
| :--- | :--- | :--- | :--- | :--- |
| `test_sanitize_whitespace` | `TextCleaner.sanitize_whitespace` | Unit | Mixed whitespace, tabs, and newlines | Collapses repeated whitespace into single spaces |
| `test_slugify` | `TextCleaner.slugify` | Unit | Special characters & mixed case | Returns lowercase alphanumeric hyphenated slug |
| `test_mask_email_valid` | `TextCleaner.mask_email` | Unit | Standard RFC email string | Replaces middle username characters with asterisks |
| `test_mask_email_invalid` | `TextCleaner.mask_email` | Edge / Error | String missing `@` | Raises `ValueError` |
| `test_compute_mean` | `MetricsCalculator.compute_mean` | Unit / Edge | Valid float list & empty list | Computes average; raises `ValueError` on empty list |
| `test_compute_median` | `MetricsCalculator.compute_median` | Unit | Odd & even length sequences | Computes exact middle or average of middle pair |
| `test_compute_stdev` | `MetricsCalculator.compute_stdev` | Unit / Edge | 8 observations & single item | Computes sample stdev; raises `ValueError` if $N < 2$ |
| `test_detect_iqr_outliers`| `MetricsCalculator.detect_iqr_outliers` | Unit | Distribution with extreme value (100) | Identifies 100 as outlier using $1.5 \times IQR$ rule |
| `test_validation_missing` | `DataPipeline.validate_record` | Error | Dict missing required key `email` | Raises `ValidationError` with descriptive message |
| `test_validation_negative`| `DataPipeline.validate_record` | Error | Dict with `amount = -10.0` | Raises `ValidationError` preventing invalid revenue |
| `test_pipeline_e2e` | `DataPipeline.process_records` | Integration | Mixed batch (valid & corrupted items) | Rejects bad records, cleans valid ones, aggregates metrics |

---

## 3. How to Run the Test Suite
```bash
# Execute the Week 3 automated test suite
python -m unittest week3_testing.test_engine -v
```

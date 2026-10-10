import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls
import os

doc = docx.Document()

# Page setup - Standard 1 inch margins
for section in doc.sections:
    section.top_margin = Inches(1)
    section.bottom_margin = Inches(1)
    section.left_margin = Inches(1)
    section.right_margin = Inches(1)

def set_run_font(run, name='Calibri', size=11, color=None, bold=False, italic=False):
    run.font.name = name
    run.font.size = Pt(size)
    run.bold = bold
    run.italic = italic
    if color:
        run.font.color.rgb = color

def add_title(text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(4)
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run(text)
    set_run_font(r, 'Calibri', 24, RGBColor(26, 54, 93), bold=True)
    return p

def add_subtitle(text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(16)
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run(text)
    set_run_font(r, 'Calibri', 12, RGBColor(74, 85, 104), italic=True)
    return p

def add_h1(text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(16)
    p.paragraph_format.space_after = Pt(6)
    p.paragraph_format.keep_with_next = True
    r = p.add_run(text)
    set_run_font(r, 'Calibri', 15, RGBColor(31, 78, 121), bold=True)
    return p

def add_h2(text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(11)
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.keep_with_next = True
    r = p.add_run(text)
    set_run_font(r, 'Calibri', 12.5, RGBColor(43, 108, 176), bold=True)
    return p

def add_p(text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(6)
    p.paragraph_format.line_spacing = 1.15
    r = p.add_run(text)
    set_run_font(r, 'Calibri', 11, RGBColor(45, 55, 72))
    return p

def add_bullet(bold_prefix, text):
    p = doc.add_paragraph(style='List Bullet')
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(3)
    p.paragraph_format.line_spacing = 1.15
    r1 = p.add_run(bold_prefix + ' ')
    set_run_font(r1, 'Calibri', 11, RGBColor(26, 32, 44), bold=True)
    r2 = p.add_run(text)
    set_run_font(r2, 'Calibri', 11, RGBColor(45, 55, 72))
    return p

def add_code_block(code_text):
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = tbl.cell(0, 0)
    shd = parse_xml(r'<w:shd {} w:fill="F7FAFC"/>'.format(nsdecls('w')))
    cell._tc.get_or_add_tcPr().append(shd)
    borders = parse_xml(r'<w:tcBorders {}><w:top w:val="single" w:sz="4" w:space="0" w:color="CBD5E0"/><w:left w:val="single" w:sz="24" w:space="0" w:color="3182CE"/><w:bottom w:val="single" w:sz="4" w:space="0" w:color="CBD5E0"/><w:right w:val="single" w:sz="4" w:space="0" w:color="CBD5E0"/></w:tcBorders>'.format(nsdecls('w')))
    cell._tc.get_or_add_tcPr().append(borders)
    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(4)
    p.paragraph_format.space_after = Pt(4)
    r = p.add_run(code_text)
    set_run_font(r, 'Consolas', 9.5, RGBColor(45, 55, 72))
    doc.add_paragraph().paragraph_format.space_after = Pt(4)

def add_callout(title, body):
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = tbl.cell(0, 0)
    shd = parse_xml(r'<w:shd {} w:fill="EDF2F7"/>'.format(nsdecls('w')))
    cell._tc.get_or_add_tcPr().append(shd)
    borders = parse_xml(r'<w:tcBorders {}><w:top w:val="none"/><w:left w:val="single" w:sz="24" w:space="0" w:color="2B6CB0"/><w:bottom w:val="none"/><w:right w:val="none"/></w:tcBorders>'.format(nsdecls('w')))
    cell._tc.get_or_add_tcPr().append(borders)
    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(4)
    p.paragraph_format.space_after = Pt(2)
    r1 = p.add_run(title + '\n')
    set_run_font(r1, 'Calibri', 10.5, RGBColor(43, 108, 176), bold=True)
    r2 = p.add_run(body)
    set_run_font(r2, 'Calibri', 10, RGBColor(74, 85, 104), italic=True)
    doc.add_paragraph().paragraph_format.space_after = Pt(4)

# Document Header
add_title('Writing Automated Tests for Python Applications')
add_subtitle('Week 3 Milestone Task: Test-Driven Development (TDD), Unit & Integration Testing, and Quality Assurance\nJunior Python Developer Virtual Internship — Yuva Learn Certification\nPrepared by: Pratyaksh (@Pratyaksh82)')

# Metadata Table
meta_tbl = doc.add_table(rows=5, cols=2)
meta_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
meta_data = [
    ("Candidate Name", "Pratyaksh"),
    ("Program & Role", "Junior Python Developer Certification (Yuva Learn)"),
    ("Submission Milestone", "Week 3: Writing Automated Tests for Python Applications"),
    ("Source Code Repository", "https://github.com/Pratyaksh82/python-internship.git"),
    ("Execution Environment", "Python 3.14+ (unittest, coverage, standard library)")
]
for i, (k, v) in enumerate(meta_data):
    c0 = meta_tbl.cell(i, 0)
    c1 = meta_tbl.cell(i, 1)
    c0.paragraphs[0].text = k
    set_run_font(c0.paragraphs[0].runs[0], 'Calibri', 10, RGBColor(26, 54, 93), bold=True)
    c1.paragraphs[0].text = v
    set_run_font(c1.paragraphs[0].runs[0], 'Calibri', 10, RGBColor(45, 55, 72))
    shd = parse_xml(r'<w:shd {} w:fill="F7FAFC"/>'.format(nsdecls('w')))
    c0._tc.get_or_add_tcPr().append(shd)

doc.add_paragraph().paragraph_format.space_after = Pt(6)

# Section 1
add_h1('1. Executive Summary & Quality Assurance Objectives')
add_p(
    'In modern software engineering, automated testing is the bedrock of dependable systems. As codebases expand, '
    'manual quality assurance fails to prevent regressions, edge case failures, and performance bottlenecks. '
    'The Week 3 milestone of the Junior Python Developer Virtual Internship centers on mastering Test-Driven Development (TDD), '
    'architecting testable modules, establishing unit and integration test suites using Python’s standard unittest framework, '
    'and validating error containment across boundary conditions.'
)
add_p(
    'To fulfill this objective, a moderately complex data processing, sanitization, and analytics engine '
    '(week3_testing/engine.py) was developed alongside an automated test suite (week3_testing/test_engine.py). '
    'The system incorporates three cohesive sub-modules: string cleaning and PII privacy masking (TextCleaner), '
    'mathematical and statistical metrics calculation (MetricsCalculator), and an end-to-end batch validation pipeline (DataPipeline). '
    'All units were designed and verified following strict TDD workflows, achieving high defect prevention and sub-millisecond execution.'
)

# Section 2
add_h1('2. Test-Driven Development (TDD) Lifecycle & Architecture')
add_p(
    'Test-Driven Development inverts the traditional paradigm of writing application code first and testing afterwards. '
    'By establishing test requirements beforehand, developers clarify specifications, eliminate dead code, '
    'and ensure exceptional modularity and testability. The process follows the disciplined Red-Green-Refactor loop.'
)

add_h2('2.1 The Red-Green-Refactor Cycle')
add_bullet('1. Red Phase (Specification):', 'A test case is authored to define an expected capability, invariant, or edge condition. Running the test confirms failure, validating that the test is sensitive to the missing implementation and preventing false positives.')
add_bullet('2. Green Phase (Minimal Implementation):', 'The minimal functional code necessary to satisfy the test assertions is authored. The test suite is re-executed to verify that the test transitions from failing to passing cleanly.')
add_bullet('3. Refactor Phase (Optimization):', 'The implementation is refactored to optimize performance, remove duplication, enhance type readability, and enforce clean design without altering external behavior, with passing tests serving as a safety net.')

add_h2('2.2 Comparative Analysis: TDD vs. Test-After vs. BDD')
add_p(
    'In traditional "Test-After" development, engineers author tests after completing the module. This frequently leads to '
    'tightly coupled code that is difficult to isolate, missing edge cases, and reduced test coverage due to cognitive bias. '
    'In contrast, TDD forces the developer to act as the first consumer of the API, designing ergonomic function signatures, '
    'clear return types, and explicit exception boundaries. Behavior-Driven Development (BDD) builds upon TDD by phrasing '
    'specifications in human-readable Given-When-Then syntax, commonly used in business-facing end-to-end integration workflows.'
)

# Section 3
add_h1('3. Architecture and Implementation of Tested Modules')
add_p(
    'The target module (week3_testing/engine.py) is architected specifically for high testability. '
    'It features pure functions, zero mutable global state, explicit custom exception hierarchies, and deterministic execution.'
)

add_h2('3.1 String Sanitization & Privacy: TextCleaner')
add_p(
    'TextCleaner provides static string transformation utilities designed to clean dirty user input and protect personally '
    'identifiable information (PII). Its functions operate with strict type validation, immediately rejecting non-string inputs '
    'with TypeError to maintain defensive boundaries.'
)
add_bullet('sanitize_whitespace(text):', 'Utilizes regular expression pattern r"\\s+" to collapse repeated spaces, tabs, and newlines into single spaces, followed by trimming external whitespace.')
add_bullet('slugify(text):', 'Converts arbitrary titles or product names into URL-safe strings by stripping non-alphanumeric symbols, converting to lowercase, and replacing spaces with single hyphens.')
add_bullet('mask_email(email):', 'Protects customer email addresses by preserving the first and last characters of the username while replacing intermediate characters with asterisks (e.g. "p******h@example.com"). Validates standard RFC email formats and raises ValueError on malformed inputs.')

add_h2('3.2 Statistical Computations: MetricsCalculator')
add_p(
    'MetricsCalculator encapsulates mathematical aggregations and anomaly detection. Because statistical routines '
    'can easily encounter numerical edge cases (such as empty inputs or zero degrees of freedom), every method enforces '
    'explicit boundary checks.'
)
add_bullet('compute_mean(numbers):', 'Calculates the arithmetic average. Raises ValueError when invoked with an empty list, preventing silent ZeroDivisionError occurrences.')
add_bullet('compute_median(numbers):', 'Sorts numeric sequences and handles both odd-length (exact middle index) and even-length (mean of middle two elements) collections.')
add_bullet('compute_stdev(numbers):', 'Computes the sample standard deviation with n-1 degrees of freedom using the math.sqrt module. Enforces that at least two observations are present, raising ValueError otherwise.')
add_bullet('detect_iqr_outliers(numbers):', 'Applies non-parametric outlier detection via the Interquartile Range (IQR). Computes the first quartile (Q1) and third quartile (Q3), deriving the IQR = Q3 - Q1. Values falling outside the fence [Q1 - 1.5*IQR, Q3 + 1.5*IQR] are flagged as statistical anomalies.')

add_h2('3.3 Batch Validation & Transformation: DataPipeline')
add_p(
    'DataPipeline coordinates end-to-end processing across raw input records. It enforces required field existence '
    '(id, name, email, amount), verifies numeric non-negativity, sanitizes string fields, masks emails, and computes '
    'aggregate batch metrics, gracefully routing malformed records to a rejection counter without aborting the batch.'
)

# Section 4
add_h1('4. Test Suite Specification & Coverage Matrix')
add_p(
    'The automated test suite in week3_testing/test_engine.py includes 11 focused test cases covering unit assertions, '
    'boundary values, error conditions, and end-to-end integration flows.'
)

test_tbl = doc.add_table(rows=12, cols=4)
test_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
headers = ["Test Method", "Scope", "Input Condition", "Expected Invariant / Assertion"]
for j, h in enumerate(headers):
    c = test_tbl.cell(0, j)
    c.paragraphs[0].text = h
    set_run_font(c.paragraphs[0].runs[0], 'Calibri', 10, RGBColor(255, 255, 255), bold=True)
    shd = parse_xml(r'<w:shd {} w:fill="2B6CB0"/>'.format(nsdecls('w')))
    c._tc.get_or_add_tcPr().append(shd)

matrix_data = [
    ("test_sanitize_whitespace", "Unit", "String with tabs, extra spaces, newlines", "Collapses to single whitespace and trimmed borders"),
    ("test_slugify", "Unit", "'Python Automated Testing 2026!'", "Normalizes to 'python-automated-testing-2026'"),
    ("test_mask_email_valid", "Unit", "'pratyaksh@example.com'", "Masks middle characters with asterisks: 'p******h@example.com'"),
    ("test_mask_email_invalid_format", "Error", "'invalid-email-address' (no @)", "Raises ValueError preventing corrupted data ingestion"),
    ("test_compute_mean_and_empty", "Unit/Edge", "Valid floats & empty list []", "Calculates mean 20.0; raises ValueError on empty list"),
    ("test_compute_median_odd_even", "Unit", "[1, 5, 2] and [1, 2, 3, 4]", "Asserts 2.0 on odd and 2.5 on even length sequences"),
    ("test_compute_stdev", "Unit/Edge", "8 observations vs 1 observation", "Asserts stdev 5.237; raises ValueError when N < 2"),
    ("test_detect_iqr_outliers", "Unit", "Distribution containing value 100", "Identifies 100 as outlier using 1.5 * IQR fence"),
    ("test_validation_rejects_missing", "Error", "Dict missing 'email' field", "Raises custom ValidationError with field message"),
    ("test_validation_rejects_negative", "Error", "Dict with 'amount': -10.0", "Raises custom ValidationError preventing negative values"),
    ("test_end_to_end_pipeline", "Integration", "Batch of 3 records (2 valid, 1 corrupt)", "Processes 3, validates 2, rejects 1, aggregates revenue")
]

for i, (m, sc, inp, exp) in enumerate(matrix_data, start=1):
    c0 = test_tbl.cell(i, 0)
    c1 = test_tbl.cell(i, 1)
    c2 = test_tbl.cell(i, 2)
    c3 = test_tbl.cell(i, 3)
    c0.paragraphs[0].text = m
    c1.paragraphs[0].text = sc
    c2.paragraphs[0].text = inp
    c3.paragraphs[0].text = exp
    set_run_font(c0.paragraphs[0].runs[0], 'Consolas', 9, RGBColor(26, 54, 93))
    set_run_font(c1.paragraphs[0].runs[0], 'Calibri', 9, RGBColor(45, 55, 72))
    set_run_font(c2.paragraphs[0].runs[0], 'Calibri', 9, RGBColor(74, 85, 104))
    set_run_font(c3.paragraphs[0].runs[0], 'Calibri', 9, RGBColor(40, 116, 166))
    if i % 2 == 1:
        shd = parse_xml(r'<w:shd {} w:fill="F7FAFC"/>'.format(nsdecls('w')))
        c0._tc.get_or_add_tcPr().append(shd)
        c1._tc.get_or_add_tcPr().append(shd)
        c2._tc.get_or_add_tcPr().append(shd)
        c3._tc.get_or_add_tcPr().append(shd)

doc.add_paragraph().paragraph_format.space_after = Pt(6)

# Section 5
add_h1('5. Automated Test Execution Results')
add_p(
    'The automated tests execute via Python’s standard unittest test runner. All 11 test cases pass in under 2 milliseconds.'
)

add_code_block(
    "======================================================================\n"
    "Test Run: Python 3.14 (unittest)\n"
    "Command: python -m unittest week3_testing.test_engine -v\n"
    "----------------------------------------------------------------------\n"
    "test_end_to_end_pipeline_processing (TestDataPipelineIntegration) ... ok\n"
    "test_validation_rejects_missing_field (TestDataPipelineIntegration) ... ok\n"
    "test_validation_rejects_negative_amount (TestDataPipelineIntegration) ... ok\n"
    "test_compute_mean_and_empty_guard (TestMetricsCalculator) ... ok\n"
    "test_compute_median_odd_and_even (TestMetricsCalculator) ... ok\n"
    "test_compute_stdev (TestMetricsCalculator) ... ok\n"
    "test_detect_iqr_outliers (TestMetricsCalculator) ... ok\n"
    "test_mask_email_invalid_format_raises_error (TestTextCleaner) ... ok\n"
    "test_mask_email_valid (TestTextCleaner) ... ok\n"
    "test_sanitize_whitespace (TestTextCleaner) ... ok\n"
    "test_slugify (TestTextCleaner) ... ok\n"
    "----------------------------------------------------------------------\n"
    "Ran 11 tests in 0.001s\n\n"
    "OK"
)

# Section 6
add_h1('6. Key Testing Principles, Patterns & Code Walkthrough')
add_p(
    'The implementation adheres to established industry testing patterns that ensure test durability:'
)
add_bullet('AAA Pattern (Arrange-Act-Assert):', 'Every test explicitly establishes inputs (Arrange), invokes the target method (Act), and verifies expected results (Assert), maximizing diagnostic clarity when failures occur.')
add_bullet('Negative & Exception Testing (assertRaises):', 'Negative test scenarios ensure that invalid inputs trigger expected custom exceptions (ValueError, ValidationError, TypeError) with meaningful error messages.')
add_bullet('Boundary & Edge Value Analysis:', 'Edge conditions tested include empty sequences, single-element collections, extreme outlier values, and negative monetary amounts.')
add_bullet('Deterministic Hermetic Independence:', 'Each test is isolated in its own TestCase method; tests neither share mutable state nor depend on execution sequence.')

add_h2('6.1 Deep-Dive Code Snippets & Test Invariants')
add_code_block(
    "# Testing String Sanitization & Boundary Whitespace:\n"
    "def test_sanitize_whitespace(self):\n"
    "    raw = '   John    Doe   \\n\\t  '\n"
    "    self.assertEqual(TextCleaner.sanitize_whitespace(raw), 'John Doe')\n\n"
    "# Testing Outlier Detection via Interquartile Range:\n"
    "def test_detect_iqr_outliers(self):\n"
    "    data = [10, 12, 12, 13, 12, 11, 14, 100]  # 100 is extreme outlier\n"
    "    outliers, bounds = MetricsCalculator.detect_iqr_outliers(data)\n"
    "    self.assertIn(100, outliers)\n\n"
    "# Integration Test: Batch Ingestion & Aggregation:\n"
    "def test_end_to_end_pipeline_processing(self):\n"
    "    records = [\n"
    "        {'id': 1, 'name': '  Alice Smith ', 'email': 'alice@company.com', 'amount': 100.0},\n"
    "        {'id': 2, 'name': 'Bob Jones', 'email': 'bob@org.net', 'amount': 200.0},\n"
    "        {'id': 3, 'name': 'Corrupt', 'email': 'bad_email', 'amount': -5.0}\n"
    "    ]\n"
    "    summary = self.pipeline.process_records(records)\n"
    "    self.assertEqual(summary['valid_count'], 2)\n"
    "    self.assertEqual(summary['rejected_count'], 1)\n"
    "    self.assertEqual(summary['total_revenue'], 300.0)"
)

# Section 7
add_h1('7. Mocking, Fixtures, and Test Isolation in Python')
add_p(
    'As applications scale, modules often interface with external systems such as REST APIs, databases, or file systems. '
    'In such scenarios, unit tests must remain fast, deterministic, and isolated using test doubles:'
)
add_bullet('unittest.mock.Mock & MagicMock:', 'Used to simulate complex objects, allowing assertions on method invocation counts, call arguments, and return values without invoking actual business components.')
add_bullet('unittest.mock.patch Decorators:', 'Enable dynamic monkey-patching of system calls, network requests (e.g., urllib or requests), and time functions during test execution, automatically restoring original behavior upon test exit.')
add_bullet('Pytest Fixtures & Dependency Injection:', 'When using Pytest, fixtures decorated with @pytest.fixture provide clean, reusable setup and teardown logic, cleanly injecting database handles or test configurations into test functions.')

# Section 9
add_h1('9. Test Automation in Continuous Integration (CI/CD)')
add_p(
    'In modern professional teams, automated testing forms the gating barrier for continuous delivery. '
    'By configuring GitHub Actions or GitLab CI workflows, test suites run automatically against every pull request '
    'and push event across diverse operating systems (Ubuntu, Windows, macOS) and Python interpreter versions (3.8 through 3.14). '
    'Automated coverage tools such as coverage.py or pytest-cov ensure that code quality metrics and test thresholds '
    'remain strictly enforced before any merge into production branches.'
)

# Section 10
add_h1('10. Conclusion & Week 4 Roadmap')
add_p(
    'The Week 3 milestone demonstrates the practical application of Test-Driven Development in Python engineering. '
    'By developing a robust data engine supported by comprehensive unit and integration tests, code reliability, '
    'maintainability, and regression immunity are firmly established. '
    'In Week 4, these automated testing and data engineering foundations will expand toward external APIs and web-scraping workflows.'
)

output_dir = r"c:\Users\praty\Desktop\certification\python\docs"
os.makedirs(output_dir, exist_ok=True)
output_path = os.path.join(output_dir, "Python_Automated_Testing_Week3_Report.docx")
doc.save(output_path)

total_words = 0
for p in doc.paragraphs:
    total_words += len(p.text.split())
for t in doc.tables:
    for row in t.rows:
        for cell in row.cells:
            for p in cell.paragraphs:
                total_words += len(p.text.split())

print(f"Report generated successfully at: {output_path}")
print(f"Total word count: {total_words} words")

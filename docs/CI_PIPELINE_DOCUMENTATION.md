# Continuous Integration (CI/CD) Pipeline Documentation (Week 6)

**Program:** Junior Python Developer Virtual Internship (Yuva Learn)  
**Milestone:** Week 6: Integrating Continuous Integration (CI) in Python Projects  
**Engineer:** Pratyaksh ([@Pratyaksh82](https://github.com/Pratyaksh82))  

---

## 1. Executive Summary & CI Architecture
This document details the configuration, deployment, and operational procedures for the automated Continuous Integration (CI) pipeline integrated into the `python-internship` repository using **GitHub Actions**. The pipeline guarantees software quality, regression immunity, and security standards by enforcing automated quality gates across every `git push` and `pull_request` targeting the `main` branch.

```mermaid
graph TD
    Push([git push / PR to main]) --> Trigger[GitHub Actions Workflow: ci.yml]
    Trigger --> Matrix{Matrix Runners: Ubuntu & Windows x Python 3.11, 3.12}
    Matrix --> Checkout[actions/checkout@v4]
    Checkout --> Setup[actions/setup-python@v5]
    Setup --> Install[pip install flake8 bandit coverage]
    Install --> Lint[Stage 1: Linting PEP 8 via flake8]
    Lint --> Sec[Stage 2: SAST Security Audit via Bandit]
    Sec --> Test1[Stage 3: Week 1 To-Do CLI Unit Tests]
    Test1 --> Test3[Stage 4: Week 3 TDD Data Engine Tests]
    Test3 --> Test4[Stage 5: Week 4 Performance Benchmark]
    Test4 --> Test5[Stage 6: Week 5 Security Attack Simulation]
    Test5 --> Cov[Stage 7: Test Coverage & Artifact Reporting]
    Cov --> Pass([Build Status: PASS / Green Badge])
```

---

## 2. Automated Quality Gates

### Stage 1: Static Code Linting (`flake8`)
- **Scope:** Enforces PEP 8 style conventions, flags undefined variables (`F82`), syntax errors (`E9`), and structural complexity violations.
- **Rules:** Restricts line length to 127 characters and cyclomatic complexity to $\le 15$.

### Stage 2: Security Static Analysis (`bandit`)
- **Scope:** Scans Python AST for security vulnerabilities across `todo/`, `week2_debugging/`, `week3_testing/`, `week4_optimization/`, and `week5_security/`.
- **Detections:** Detects unsafe subprocess calls (B602), insecure deserialization (B301), and weak cryptography (B303).

### Stage 3-6: Automated Milestone Test Suites
- **Week 1:** Validates 17 unit tests for To-Do List CLI models, managers, and atomic JSON persistence.
- **Week 3:** Validates 11 unit and integration tests for data cleaning, statistical metrics, and batch pipelines.
- **Week 4:** Profiles performance benchmarks ensuring 380x+ execution speedup and zero discrepancy.
- **Week 5:** Executes 6 real-world attack simulations confirming that SQLi, path traversal, and command injection remain blocked.

### Stage 7: Coverage Aggregation (`coverage.py`)
- Analyzes statement execution coverage, ensuring zero regressions across core business logic.

---

## 3. How to Execute the CI Pipeline Locally

Developers can validate the complete CI pipeline locally before pushing commits using the automated local CI runner:

```bash
# Clone the repository
git clone https://github.com/Pratyaksh82/python-internship.git
cd python-internship

# Run the complete local CI suite
python scripts/run_local_ci.py
```

### Local CI Execution Summary:
```text
======================================================================
 EXECUTING LOCAL CONTINUOUS INTEGRATION (CI) PIPELINE
======================================================================
[PASSED] Stage 'Week 1 To-Do List CLI Unit Tests' succeeded in 0.18s
[PASSED] Stage 'Week 2 Debugging Verification Suite' succeeded in 0.11s
[PASSED] Stage 'Week 3 Data Engine & TDD Unit Tests' succeeded in 0.13s
[PASSED] Stage 'Week 4 Performance Profiler & Benchmark' succeeded in 2.59s
[PASSED] Stage 'Week 5 Security Audit & Attack Simulation' succeeded in 0.73s
======================================================================
[SUCCESS] ALL CI PIPELINE STAGES PASSED SUCCESSFULLY!
======================================================================
```

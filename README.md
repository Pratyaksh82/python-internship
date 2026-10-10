# Python Internship Certification Program

[![Python Version](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Active-brightgreen.svg)]()
[![Tests](https://img.shields.io/badge/Tests-17%20Passed-success.svg)]()

Welcome to the **Python Internship Certification Program** repository. This repository houses all project milestones, architectural designs, modular source code, and comprehensive documentation developed during the Junior Python Developer Virtual Internship on the **Yuva Learn** certification platform.

- **Author:** Pratyaksh ([@Pratyaksh82](https://github.com/Pratyaksh82))
- **Primary Language:** Python 3.14+ (Standard Library, Zero External Dependencies)
- **Repository:** [python-internship](https://github.com/Pratyaksh82/python-internship)

---

## 📂 Certification Roadmap

| Milestone | Task Title | Core Technologies | Status |
| :--- | :--- | :--- | :---: |
| **Week 1** | **Python CLI Application Design and Implementation** | OOP, Dataclasses, Atomic JSON, Unit Testing | ✅ Completed |
| **Week 2** | **Debugging and Troubleshooting Python Applications** | pdb, Runtime Tracing, Root-Cause Analysis, Refactoring | ✅ Completed |
| **Week 3** | *Upcoming Milestone* | Advanced File I/O & Networking | ⏳ Upcoming |
| **Week 4** | *Upcoming Milestone* | Web Scraping / API Integration | ⏳ Upcoming |
| **Week 5** | *Upcoming Milestone* | Database Integration / ORM | ⏳ Upcoming |
| **Week 6** | *Upcoming Milestone* | Final Capstone Engineering Project | ⏳ Upcoming |

---

## 📝 Week 1: Python CLI Application Design & Implementation (To-Do List Manager)

### Overview
Week 1 delivers a modular, object-oriented **Command-Line Interface (CLI) To-Do List Manager**. Built entirely with Python's standard library, it emphasizes clean architecture, separation of concerns, defensive input validation, atomic data persistence, and automated test coverage.

### Key Features
- **Full CRUD Capabilities:** Add, list, inspect, edit, and delete tasks.
- **Priority Management:** Categorize tasks into `LOW`, `MEDIUM`, and `HIGH` priority levels with visual indicators.
- **Atomic JSON Storage:** Uses a write-to-temp-then-swap pattern (`os.replace`) to guarantee zero file corruption even upon unexpected system interruption.
- **Corrupted File Auto-Recovery:** Gracefully catches malformed JSON files, logs actionable warnings, and recovers without unhandled crashes.
- **Search & Multi-Field Filtering:** Search tasks by keyword across both titles and descriptions; filter by `PENDING` or `COMPLETED` status.
- **Productivity Analytics:** Displays total tasks, completed percentages, pending items, and priority distribution breakdowns.
- **Cross-Platform Console Compatibility:** Explicit UTF-8 stdout configuration with fallback replacement ensures error-free rendering on legacy Windows `cp1252` terminals.
- **100% Zero External Dependencies:** Runs natively on standard Python without requiring `pip install`.

---

## 🏛️ System Architecture

The application adopts a 4-tier layered architecture separating presentation, business logic, domain entities, and data persistence:

```mermaid
graph TD
    User([Terminal User / CLI]) -->|Console I/O| CLI[todo/cli.py: TodoCLI]
    CLI -->|Dispatches Commands| Manager[todo/manager.py: TaskManager]
    Manager -->|Manipulates Entities| Models[todo/models.py: Task & Enums]
    Manager -->|Reads / Writes Data| Storage[todo/storage.py: JSONTaskStorage]
    Storage -.->|Implements Interface| ABC[todo/storage.py: TaskStorage ABC]
    Storage -->|Atomic Persistence| Disk[(data/tasks.json)]
```

### Module Breakdown
- `main.py`: Application entrypoint; initializes dependencies, seeds initial demo tasks on fresh start, and runs the CLI loop.
- `todo/models.py`: Defines `Task` dataclass, `Priority` enum, `TaskStatus` enum, timestamp tracking, and JSON serialization.
- `todo/storage.py`: Declares `TaskStorage` abstract base class (ABC) and implements `JSONTaskStorage` with atomic file writes.
- `todo/manager.py`: Business logic orchestrator managing CRUD, sorting, filtering, keyword search, and productivity metrics.
- `todo/cli.py`: Terminal presentation layer featuring a 12-option menu, formatted ASCII table rendering, and defensive input guards.
- `tests/test_todo.py`: Automated test suite containing 17 unit tests verifying models, storage, and manager logic.
- `scripts/generate_week1_report.py`: Automated generator producing the formal 2,400+ word Word document report (`.docx`).

---

## 🚀 Quickstart & Usage

### Prerequisites
- Python 3.8 or newer (tested on Python 3.14).

### Running the Application
```bash
# Clone the repository
git clone https://github.com/Pratyaksh82/python-internship.git
cd python-internship

# Launch the interactive CLI
python main.py
```

### Interactive Menu Options
```text
-----------------------------------------------------------------------
 MAIN MENU
-----------------------------------------------------------------------
 1. ➕ Add New Task              7. ✏️  Update Task Details
 2. 📋 View All Tasks            8. 🗑️  Delete Task
 3. ⏳ View Pending Tasks        9. 🔍 Search Tasks by Keyword
 4. ✅ View Completed Tasks      10. 🧹 Clear All Completed Tasks
 5. ✔️  Mark Task as Completed    11. 📊 View Productivity Metrics
 6. 🔄 Mark Task as Pending      12. 🚪 Exit Application
-----------------------------------------------------------------------
```

---

## 🧪 Running Automated Unit Tests

The test suite validates model invariants, atomic file handling, corrupted file recovery, search algorithms, and CRUD operations:

```bash
python -m unittest discover -s tests -v
```

### Test Summary
```text
test_create_valid_task (test_todo.TestTaskModel) ... ok
test_empty_title_raises_value_error (test_todo.TestTaskModel) ... ok
test_mark_completed_and_pending (test_todo.TestTaskModel) ... ok
test_serialization_round_trip (test_todo.TestTaskModel) ... ok
test_corrupted_json_handled_gracefully (test_todo.TestJSONStorage) ... ok
test_load_non_existent_file_returns_empty_list (test_todo.TestJSONStorage) ... ok
test_save_and_load_tasks (test_todo.TestJSONStorage) ... ok
test_add_task_success (test_todo.TestTaskManager) ... ok
test_auto_incrementing_ids (test_todo.TestTaskManager) ... ok
test_clear_completed (test_todo.TestTaskManager) ... ok
test_filtering_tasks_by_status (test_todo.TestTaskManager) ... ok
test_get_task_success_and_not_found (test_todo.TestTaskManager) ... ok
test_remove_task (test_todo.TestTaskManager) ... ok
test_search_tasks (test_todo.TestTaskManager) ... ok
test_sorting_by_priority (test_todo.TestTaskManager) ... ok
test_statistics (test_todo.TestTaskManager) ... ok
test_update_task (test_todo.TestTaskManager) ... ok

----------------------------------------------------------------------
Ran 17 tests in 0.029s

OK
```

---

## 🔍 Week 2: Debugging and Troubleshooting Python Applications

### Overview
Week 2 centers on real-world troubleshooting, runtime tracing, and defensive code refactoring using Python's standard `pdb` module. An enterprise e-commerce order processor (`week2_debugging/`) was engineered to simulate 8 high-impact Python bugs across file I/O, sequences, dictionaries, scopes, and serialization.

### 8 Bugs Diagnosed & Resolved
1. **File I/O Resource Leaks:** Fixed raw `open()` calls by using `with` context managers and `os.path.exists` validation.
2. **Mutable Default Arguments:** Eliminated state leakage across function calls by replacing `items=[]` with `None` and defensive copy allocation.
3. **Off-by-One Loop Indexing:** Replaced 1-based indexing (`range(1, len+1)`) with direct Python iteration.
4. **Sequence Mutation in Iteration:** Eliminated skipped records by replacing in-place `remove()` with list comprehensions.
5. **Type Coercion & Zero-Division:** Added currency regex parsing and empty dataset length guards.
6. **Shallow Copy Mutations:** Replaced `list()` with `copy.deepcopy()` to isolate historical snapshots.
7. **Scoping & Variable Shadowing:** Standardized upfront variable initialization to eliminate `UnboundLocalError`.
8. **JSON Serialization Failures:** Implemented `DateTimeEncoder` inheriting `json.JSONEncoder` for ISO-8601 formatting.

### Running Week 2 Scripts
```bash
# Run automated bug diagnosis and verification script
python -m week2_debugging.debug_session

# Run corrected, refactored production engine
python -m week2_debugging.corrected_application
```

---

## 📄 Documentation & Deliverables

### Week 1 Deliverables
- **Formal Report (`.docx`):** [`docs/Python_CLI_TodoList_Week1_Report.docx`](docs/Python_CLI_TodoList_Week1_Report.docx) (2,444 words).
- **Source Code Archive (`.zip`):** [`docs/todo-cli-week1.zip`](docs/todo-cli-week1.zip).

### Week 2 Deliverables
- **Formal Report (`.docx`):** [`docs/Python_Debugging_Troubleshooting_Week2_Report.docx`](docs/Python_Debugging_Troubleshooting_Week2_Report.docx) (1,592 words).
- **Debugging Audit Log (`.md`):** [`week2_debugging/DEBUGGING_LOG.md`](week2_debugging/DEBUGGING_LOG.md).
- **Source Code & Log Archive (`.zip`):** [`docs/python-week2-debugging.zip`](docs/python-week2-debugging.zip).

---

## 👤 Author
- **Pratyaksh** — [@Pratyaksh82](https://github.com/Pratyaksh82)
- Program: Junior Python Developer Virtual Internship (Yuva Learn)

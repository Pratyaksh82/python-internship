# Comprehensive Debugging and Troubleshooting Log (Week 2)

**Program:** Junior Python Developer Virtual Internship (Yuva Learn)  
**Milestone:** Week 2: Debugging and Troubleshooting Python Applications  
**Engineer:** Pratyaksh ([@Pratyaksh82](https://github.com/Pratyaksh82))  

---

## 1. Executive Summary & Debugging Methodology
This log documents the identification, reproduction, root-cause isolation, and resolution of 8 high-impact bugs found in the e-commerce order processing and analytics engine (`week2_debugging/`). The debugging procedure employed Python's built-in debugger (`pdb`), exception stack-trace inspection, unit assertions, and defensive refactoring.

### Debugging Workflow Applied:
1. **Symptom Observation:** Reproduce the unhandled exception or silent data corruption.
2. **Hypothesis Formulation:** Analyze scope, variable lifetimes, reference semantics, and type boundaries.
3. **Interactive Tracing (`pdb`):** Set breakpoints (`pdb.set_trace()`), examine local frame states (`locals()`, `p var`), and step through instructions (`n`, `s`, `c`).
4. **Targeted Refactoring:** Apply clean fixes ensuring backward compatibility and zero unintended side effects.
5. **Regression Verification:** Validate with automated diagnostics script.

---

## 2. Bug Audit & Step-by-Step Resolution

### Bug 1: Unhandled FileNotFoundError & Resource Descriptor Leak
- **File & Function:** `buggy_application.py` -> `load_raw_orders(filepath)`
- **Symptom & Error:** `FileNotFoundError: [Errno 2] No such file or directory` + unclosed OS file descriptor.
- **Root Cause Hypothesis:** File opened with raw `open()` without a `try/finally` block or context manager (`with`). Missing files terminate execution with unhandled crashes.
- **pdb Diagnostic Steps:**
  ```python
  import pdb; pdb.set_trace()
  # (Pdb) n -> crashes on open(filepath, "r")
  ```
- **Code Diff:**
  ```diff
  -def load_raw_orders(filepath):
  -    f = open(filepath, "r")
  -    content = f.read()
  -    return json.loads(content)
  +def load_raw_orders(filepath: str) -> List[Dict[str, Any]]:
  +    if not os.path.exists(filepath):
  +        logger.warning("Target file '%s' does not exist.", filepath)
  +        return []
  +    with open(filepath, "r", encoding="utf-8") as f:
  +        return json.load(f)
  ```
- **Resolution & Optimization:** Integrated `os.path.exists` check, `with open(...)` context manager, and graceful empty list fallback.

---

### Bug 2: Mutable Default Argument in Function Signature
- **File & Function:** `buggy_application.py` -> `create_order(order_id, customer, items=[])`
- **Symptom:** Cross-order state pollution. Subsequent orders without items inherited items from previous orders.
- **Root Cause Hypothesis:** Python evaluates default parameter expressions once at function definition time, binding a single mutable `list` instance across all invocations.
- **Code Diff:**
  ```diff
  -def create_order(order_id, customer, items=[]):
  -    items.append({"name": "Processing Fee", "price": "1.50"})
  +def create_order(order_id: int, customer: str, items: Optional[List[Dict[str, Any]]] = None) -> Dict[str, Any]:
  +    order_items = [] if items is None else copy.deepcopy(items)
  +    order_items.append({"name": "Processing Fee", "price": 1.50})
  ```
- **Resolution & Optimization:** Defaulted `items` to `None`, instantiating a fresh list on each call.

---

### Bug 3: Off-by-One Loop Indexing Error
- **File & Function:** `buggy_application.py` -> `process_orders_batch(order_list)`
- **Symptom & Error:** `IndexError: list index out of range`.
- **Root Cause Hypothesis:** Using 1-based indexing (`range(1, len(order_list) + 1)`) against a 0-indexed Python list.
- **Code Diff:**
  ```diff
  -for i in range(1, len(order_list) + 1):
  -    order = order_list[i]
  +for order in order_list:
  +    processed.append(copy.deepcopy(order))
  ```
- **Resolution & Optimization:** Replaced range indexing with idiomatic Python direct iteration.

---

### Bug 4: Mutating a List While Iterating Over It
- **File & Function:** `buggy_application.py` -> `filter_cancelled_orders(orders)`
- **Symptom:** Consecutive cancelled orders were skipped because `orders.remove(order)` shifted indices leftward during iteration.
- **Root Cause Hypothesis:** Modifying a sequence while iterating disrupts the internal iterator index.
- **Code Diff:**
  ```diff
  -for order in orders:
  -    if order.get("status") == "CANCELLED":
  -        orders.remove(order)
  -return orders
  +return [order for order in orders if order.get("status") != "CANCELLED"]
  ```
- **Resolution & Optimization:** Switched to a clean list comprehension producing a new filtered sequence in $O(n)$ time.

---

### Bug 5: Unsafe Float Coercion & ZeroDivisionError
- **File & Function:** `buggy_application.py` -> `compute_average_order_value(orders)`
- **Symptom & Error:** `ZeroDivisionError: division by zero` when orders list is empty, and `ValueError: could not convert string to float: '$19.99'`.
- **Root Cause Hypothesis:** Assumed non-empty list and unformatted numeric strings.
- **Code Diff:**
  ```diff
  -for item in order["items"]:
  -    total += float(item["price"])
  -return total / len(orders)
  +if not orders:
  +    return 0.0
  +total_value = sum(sum(parse_price(i.get("price")) for i in o.get("items", [])) for o in orders)
  +return round(total_value / len(orders), 2)
  ```
- **Resolution & Optimization:** Added regex sanitizer `parse_price()` and an empty dataset guard returning `0.0`.

---

### Bug 6: Shallow Copy Mutation of Nested Data
- **File & Function:** `buggy_application.py` -> `archive_orders_snapshot(orders)`
- **Symptom:** Mutating snapshot dictionaries simultaneously mutated original active orders.
- **Root Cause Hypothesis:** `list(orders)` only shallow-copies dictionary references.
- **Code Diff:**
  ```diff
  -snapshot = list(orders)
  +snapshot = copy.deepcopy(orders)
  ```
- **Resolution & Optimization:** Employed `copy.deepcopy()` to enforce absolute memory decoupling.

---

### Bug 7: Variable Shadowing / UnboundLocalError
- **File & Function:** `buggy_application.py` -> `calculate_tax(subtotal)`
- **Symptom & Error:** `UnboundLocalError: cannot access local variable 'tax' where it is not associated with a value`.
- **Root Cause Hypothesis:** Variable `tax` was referenced in `elif` before assignment.
- **Code Diff:**
  ```diff
  -if subtotal > 100:
  -    tax = subtotal * tax_rate
  -elif subtotal > 0:
  -    tax = tax + (subtotal * 0.05)
  +if subtotal <= 0:
  +    return 0.0
  +tax = subtotal * tax_rate if subtotal > 100 else subtotal * 0.05
  +return round(tax, 2)
  ```
- **Resolution & Optimization:** Standardized early return and upfront variable assignment.

---

### Bug 8: Datetime Object JSON Serialization Failure
- **File & Function:** `buggy_application.py` -> `export_report_to_json(filepath, report_data)`
- **Symptom & Error:** `TypeError: Object of type datetime is not JSON serializable`.
- **Root Cause Hypothesis:** Standard `json.dump()` does not serialize native `datetime.datetime` objects without a custom encoder.
- **Code Diff:**
  ```diff
  -json.dump(report_data, f, indent=4)
  +class DateTimeEncoder(json.JSONEncoder):
  +    def default(self, obj):
  +        if isinstance(obj, datetime):
  +            return obj.isoformat()
  +        return super().default(obj)
  +json.dump(report_data, f, indent=4, cls=DateTimeEncoder)
  ```
- **Resolution & Optimization:** Implemented `DateTimeEncoder` inheriting from `json.JSONEncoder` converting datetimes to ISO 8601 strings.

---

## 3. Verification & Execution Status
- All 8 bugs were reproduced in `week2_debugging/debug_session.py`.
- Corrected code validated with 100% success without unexpected termination.

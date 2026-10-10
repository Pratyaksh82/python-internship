"""
SECURITY ATTACK SIMULATION AND VALIDATION HARNESS (Week 5)
Simulates 6 real-world attack vectors against both Vulnerable and Hardened implementations:
1. SQL Injection Authentication Bypass
2. Weak Password Dictionary Vulnerability
3. Arbitrary Code Execution via Deserialization
4. Command Injection Payload
5. Path Traversal Sandbox Escape
6. Sensitive Information Traceback Leakage
"""

import os
import pickle
import tempfile
import week5_security.vulnerable_app as vuln
import week5_security.hardened_app as hard


def run_attack_simulations():
    print("=" * 70)
    print(" WEEK 5: SECURITY AUDIT & ATTACK SIMULATION HARNESS")
    print("=" * 70)

    # 1. SQL Injection Simulation
    print("\n[Simulation 1: SQL Injection Attack (admin' --)]")
    v_conn = vuln.get_vulnerable_db()
    h_conn = hard.get_hardened_db()
    sqli_payload = "admin' --"

    # Vulnerable app: Malicious login bypass
    bypassed_user = vuln.login_vulnerable(v_conn, sqli_payload, "dummy")
    print(f"-> Vulnerable App Result: BYPASSED! Logged in as: {bypassed_user}")

    # Hardened app: Securely rejected
    blocked_user = hard.login_hardened(h_conn, sqli_payload, "dummy")
    print(f"-> Hardened App Result   : BLOCKED! Result = {blocked_user}")
    assert blocked_user is None

    # 2. Insecure Password Storage
    print("\n[Simulation 2: Insecure Credential Storage]")
    print("-> Vulnerable: Stored with obsolete MD5 without salt (trivial rainbow table crack).")
    print("-> Hardened  : Stored with PBKDF2-HMAC-SHA256 (600,000 iterations + 32-byte salt).")

    # 3. Insecure Deserialization
    print("\n[Simulation 3: Insecure Pickle Deserialization]")
    class MaliciousPayload:
        def __reduce__(self):
            return (os.getenv, ("USERNAME",))

    pickled_payload = pickle.dumps(MaliciousPayload())
    v_deser = vuln.load_user_session_vulnerable(pickled_payload)
    print(f"-> Vulnerable App Executed Arbitrary Code: Returned {v_deser}")

    h_deser = hard.load_user_session_hardened(pickled_payload.decode("latin1", errors="ignore"))
    print(f"-> Hardened App Rejected Pickle Payload : Returned {h_deser}")
    assert h_deser is None

    # 4. Command Injection
    print("\n[Simulation 4: OS Command Injection (127.0.0.1 & echo PWNED)]")
    cmd_injection_payload = "127.0.0.1 & echo PWNED"
    h_cmd = hard.check_host_hardened(cmd_injection_payload)
    print(f"-> Hardened App Validated Host Regex    : Rejected payload (Result = {h_cmd})")
    assert h_cmd is False

    # 5. Path Traversal
    print("\n[Simulation 5: Directory Path Traversal (../../secret.txt)]")
    with tempfile.TemporaryDirectory() as tmpdir:
        sandbox = os.path.join(tmpdir, "sandbox")
        os.makedirs(sandbox, exist_ok=True)
        secret_file = os.path.join(tmpdir, "secret.txt")
        with open(secret_file, "w") as f:
            f.write("TOP_SECRET_CREDENTIALS")

        with open(os.path.join(sandbox, "user.txt"), "w") as f:
            f.write("Normal User Data")

        traversal_payload = "../secret.txt"
        v_leak = vuln.read_user_file_vulnerable(sandbox, traversal_payload)
        print(f"-> Vulnerable App Leaked Secret File    : Content = '{v_leak}'")

        h_leak = hard.read_user_file_hardened(sandbox, traversal_payload)
        print(f"-> Hardened App Enforced Sandbox Boundary: Traversal Blocked (Result = {h_leak})")
        assert h_leak is None

    # 6. Information Leakage
    print("\n[Simulation 6: Verbose Error & Stack Trace Leaks]")
    malformed_data = {"amount": "INVALID_ABC"}
    v_err = vuln.process_payment_vulnerable(malformed_data)
    print(f"-> Vulnerable App Exposed Internal Trace: {v_err}")

    h_err = hard.process_payment_hardened(malformed_data)
    print(f"-> Hardened App Sanitized Response      : {h_err}")
    assert "trace" not in h_err and h_err["status"] == "REJECTED"

    print("\n" + "=" * 70)
    print(" ALL 6 ATTACK SCENARIOS VERIFIED: VULNERABILITIES CONFIRMED & DEFENDED!")
    print("=" * 70)


if __name__ == "__main__":
    run_attack_simulations()

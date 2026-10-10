"""
HARDENED APPLICATION: Secure User Authentication & Vault Service
Implements enterprise defenses against OWASP Top 10 vulnerabilities:
1. Parameterized Queries: Eliminates SQL Injection (CWE-89).
2. Modern Cryptography: PBKDF2-HMAC-SHA256 with random salt & constant-time compare (CWE-256).
3. Safe Deserialization: Restricts payloads to strictly-validated JSON (CWE-502).
4. Subprocess Isolation: Enforces regex hostname validation and shell=False (CWE-78).
5. Canonical Path Sandboxing: Prevents directory traversal using commonpath (CWE-22).
6. Sanitized Error Envelopes: Generic client messages with internal audit logging (CWE-209).
"""

import hmac
import json
import logging
import os
import re
import secrets
import sqlite3
import subprocess
from typing import Any, Dict, Optional, Tuple

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("SecurityVault")

HASH_ITERATIONS = 600000


def hash_password(password: str, salt: Optional[bytes] = None) -> Tuple[str, str]:
    """Generates PBKDF2-HMAC-SHA256 hash with a cryptographically secure 32-byte salt."""
    if salt is None:
        salt = secrets.token_bytes(32)
    key = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, HASH_ITERATIONS)
    return key.hex(), salt.hex()


def verify_password(password: str, stored_hash_hex: str, stored_salt_hex: str) -> bool:
    """Constant-time verification mitigating side-channel timing attacks."""
    salt = bytes.fromhex(stored_salt_hex)
    computed_key = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, HASH_ITERATIONS)
    return hmac.compare_digest(computed_key.hex(), stored_hash_hex)


import hashlib


def get_hardened_db() -> sqlite3.Connection:
    """Initializes in-memory database with salted PBKDF2 credentials."""
    conn = sqlite3.connect(":memory:")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE users (
            id INTEGER PRIMARY KEY,
            username TEXT UNIQUE,
            password_hash TEXT,
            salt TEXT,
            role TEXT
        )
    """)
    # Seed secure admin credentials
    admin_hash, admin_salt = hash_password("AdminSecret!2026")
    user_hash, user_salt = hash_password("UserPass!2026")

    c.execute("INSERT INTO users VALUES (1, 'admin', ?, ?, 'ADMIN')", (admin_hash, admin_salt))
    c.execute("INSERT INTO users VALUES (2, 'john', ?, ?, 'USER')", (user_hash, user_salt))
    conn.commit()
    return conn


def login_hardened(conn: sqlite3.Connection, username: str, password: str) -> Optional[Dict[str, Any]]:
    """
    Hardened authentication using parameterized query and constant-time hash comparison.
    Mitigates Bug 1 (SQLi) and Bug 2 (Insecure Passwords).
    """
    cursor = conn.cursor()
    # Parameterized query prevents SQL injection
    cursor.execute("SELECT id, username, password_hash, salt, role FROM users WHERE username = ?", (username,))
    record = cursor.fetchone()

    if not record:
        logger.warning("Failed login attempt: user '%s' not found.", username)
        return None

    uid, uname, stored_hash, stored_salt, role = record
    if verify_password(password, stored_hash, stored_salt):
        logger.info("Successful authentication for user '%s'.", uname)
        return {"id": uid, "username": uname, "role": role}

    logger.warning("Failed login attempt: invalid credentials for user '%s'.", username)
    return None


def load_user_session_hardened(serialized_json: str) -> Optional[Dict[str, Any]]:
    """
    Hardened session deserialization using safe JSON parsing.
    Mitigates Bug 3 (Insecure Pickle Deserialization).
    """
    try:
        data = json.loads(serialized_json)
        if not isinstance(data, dict):
            raise ValueError("Expected dictionary structure.")
        return data
    except (json.JSONDecodeError, ValueError) as e:
        logger.error("Session token parsing rejected: %s", e)
        return None


def check_host_hardened(target_host: str) -> bool:
    """
    Hardened host availability check with regex sanitization and shell=False.
    Mitigates Bug 4 (Command Injection).
    """
    # Strict validation: Only valid alphanumeric hostnames or IPv4 addresses
    if not re.match(r"^[a-zA-Z0-9.-]+$", target_host) or len(target_host) > 64:
        logger.error("Invalid target host rejected: '%s'", target_host)
        return False

    cmd = ["ping", "-n", "1", target_host]
    try:
        res = subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=2, shell=False)
        return res.returncode == 0
    except (subprocess.SubprocessError, OSError) as e:
        logger.error("Subprocess execution failed: %s", e)
        return False


def read_user_file_hardened(base_dir: str, user_filename: str) -> Optional[str]:
    """
    Hardened file reader using canonical path boundary resolution.
    Mitigates Bug 5 (Path Traversal).
    """
    abs_base = os.path.abspath(base_dir)
    target_path = os.path.abspath(os.path.join(abs_base, user_filename))

    # Guard: Target must strictly reside within base_dir sandbox
    if os.path.commonpath([abs_base, target_path]) != abs_base:
        logger.error("Path traversal attack detected and blocked: '%s'", user_filename)
        return None

    if not os.path.isfile(target_path):
        return None

    try:
        with open(target_path, "r", encoding="utf-8") as f:
            return f.read()
    except OSError as e:
        logger.error("Failed to read sandboxed file: %s", e)
        return None


def process_payment_hardened(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Hardened input validation with generic error envelopes.
    Mitigates Bug 6 (Information Disclosure).
    """
    try:
        if not isinstance(data, dict) or "amount" not in data:
            return {"status": "REJECTED", "message": "Invalid request payload format."}
        
        amount_val = float(data["amount"])
        if amount_val <= 0:
            return {"status": "REJECTED", "message": "Transaction amount must be positive."}
        
        return {"status": "APPROVED", "amount": round(amount_val, 2)}
    except (ValueError, TypeError) as e:
        logger.warning("Internal processing error logged safely: %s", e)
        # Client receives generic, sanitized response without stack traces
        return {"status": "REJECTED", "message": "Validation failure: Malformed numerical value."}

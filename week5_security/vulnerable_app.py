"""
VULNERABLE APPLICATION: User Authentication & Vault Service
Simulates 6 classic OWASP Python security vulnerabilities:
1. SQL Injection (raw string interpolation in queries)
2. Insecure Credential Storage (plaintext / MD5 without salt)
3. Insecure Deserialization (unsafe pickle usage)
4. OS Command Injection (shell=True subprocess execution)
5. Path Traversal (arbitrary file disclosure via unsanitized file paths)
6. Sensitive Information Disclosure (verbose raw traceback exposure)
"""

import hashlib
import os
import pickle
import sqlite3


def get_vulnerable_db():
    conn = sqlite3.connect(":memory:")
    c = conn.cursor()
    c.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, username TEXT, password TEXT, role TEXT)")
    # Vulnerability 2: Plaintext / MD5 password without salt
    c.execute("INSERT INTO users VALUES (1, 'admin', '5f4dcc3b5aa765d61d8327deb882cf99', 'ADMIN')")  # md5('password')
    c.execute("INSERT INTO users VALUES (2, 'john', 'e10adc3949ba59abbe56e057f20f883e', 'USER')")   # md5('123456')
    conn.commit()
    return conn


def login_vulnerable(conn, username, password):
    # Vulnerability 1: SQL Injection via f-string formatting
    cursor = conn.cursor()
    pwd_hash = hashlib.md5(password.encode()).hexdigest()
    query = f"SELECT id, username, role FROM users WHERE username = '{username}' AND password = '{pwd_hash}'"
    cursor.execute(query)
    user = cursor.fetchone()
    return user


def load_user_session_vulnerable(serialized_token):
    # Vulnerability 3: Insecure Deserialization via pickle
    # Arbitrary code execution can be achieved by malicious payloads
    return pickle.loads(serialized_token)


def check_host_vulnerable(target_host):
    # Vulnerability 4: OS Command Injection via shell execution
    # Payload like "127.0.0.1; whoami" executes arbitrary commands
    cmd = f"ping -n 1 {target_host}"
    return os.system(cmd)


def read_user_file_vulnerable(base_dir, user_filename):
    # Vulnerability 5: Path Traversal (Arbitrary File Read)
    # Payload "../../etc/passwd" traverses outside sandbox directory
    filepath = os.path.join(base_dir, user_filename)
    with open(filepath, "r") as f:
        return f.read()


def process_payment_vulnerable(data):
    # Vulnerability 6: Information Disclosure / Raw Traceback
    try:
        val = int(data["amount"])
        return {"status": "SUCCESS", "amount": val}
    except Exception as e:
        # Leaking internal schema details and raw exception
        return {"status": "ERROR", "trace": str(e), "internal_type": type(e).__name__}

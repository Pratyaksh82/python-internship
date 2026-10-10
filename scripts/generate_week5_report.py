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
add_title('Security Enhancements in Python Applications')
add_subtitle('Week 5 Milestone Task: OWASP Threat Modeling, Defensive Hardening, Attack Simulation, and Cryptographic Engineering\nJunior Python Developer Virtual Internship — Yuva Learn Certification\nPrepared by: Pratyaksh (@Pratyaksh82)')

# Metadata Table
meta_tbl = doc.add_table(rows=5, cols=2)
meta_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
meta_data = [
    ("Candidate Name", "Pratyaksh"),
    ("Program & Role", "Junior Python Developer Certification (Yuva Learn)"),
    ("Submission Milestone", "Week 5: Security Enhancements in Python Applications"),
    ("Source Code Repository", "https://github.com/Pratyaksh82/python-internship.git"),
    ("Security Standards", "OWASP Top 10, CWE / SANS Top 25, PBKDF2-HMAC-SHA256, Bandit")
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
add_h1('1. Executive Summary & Security Objectives')
add_p(
    'In modern digital architectures, software security is not an afterthought or an isolated layer; it must be an intrinsic '
    'property embedded directly into the software development lifecycle. Python applications are frequently deployed in '
    'critical infrastructure, web backend services, microservices, and identity management gateways. However, insecure programming '
    'practices—such as direct string interpolation in SQL queries, obsolete cryptographic algorithms, untrusted deserialization, '
    'and unchecked file paths—expose applications to catastrophic breaches, data leakage, and remote code execution (RCE).'
)
add_p(
    'The Week 5 milestone of the Junior Python Developer Virtual Internship centers on conducting a thorough security audit '
    'of a user authentication and sensitive data vault service, identifying six high-risk vulnerabilities aligned with the OWASP Top 10 '
    'and MITRE Common Weakness Enumeration (CWE), implementing defensive controls, and verifying remediations through automated '
    'adversarial attack simulations.'
)

# Section 2
add_h1('2. Security Audit & Threat Modeling Framework')
add_p(
    'Threat modeling evaluates software attack surfaces by systematically identifying potential adversaries, assets, and entry points. '
    'The audit conducted in week5_security/ investigated the application against the industry-standard OWASP Top 10 (2021) categories:'
)
add_bullet('A01:2021 Broken Access Control (CWE-22):', 'Evaluating whether unauthenticated or low-privilege users can access restricted file system resources via path traversal.')
add_bullet('A02:2021 Cryptographic Failures (CWE-256 / CWE-328):', 'Assessing password storage schemes against rainbow-table attacks, pre-computation dictionaries, and timing side-channel analysis.')
add_bullet('A03:2021 Injection (CWE-89 / CWE-78):', 'Auditing database query construction and operating system command invocations for untrusted input injection.')
add_bullet('A05:2021 Security Misconfiguration (CWE-209):', 'Examining error-handling routines to prevent internal system architecture and schema disclosure through unhandled stack traces.')
add_bullet('A08:2021 Software and Data Integrity Failures (CWE-502):', 'Auditing object deserialization protocols against arbitrary bytecode execution.')

# Section 3
add_h1('3. Vulnerability Audit Matrix & Remediation Blueprint')

vuln_tbl = doc.add_table(rows=7, cols=4)
vuln_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
headers = ["Vulnerability", "OWASP Category", "CWE ID", "Defensive Control Applied"]
for j, h in enumerate(headers):
    c = vuln_tbl.cell(0, j)
    c.paragraphs[0].text = h
    set_run_font(c.paragraphs[0].runs[0], 'Calibri', 10, RGBColor(255, 255, 255), bold=True)
    shd = parse_xml(r'<w:shd {} w:fill="2B6CB0"/>'.format(nsdecls('w')))
    c._tc.get_or_add_tcPr().append(shd)

vuln_rows = [
    ("SQL Injection (SQLi)", "A03:2021 Injection", "CWE-89", "Parameterized queries with placeholder binding"),
    ("Insecure Password Storage", "A02:2021 Cryptographic Failures", "CWE-256", "PBKDF2-HMAC-SHA256 (600,000 rounds, 32B salt)"),
    ("Insecure Deserialization", "A08:2021 Integrity Failures", "CWE-502", "Replaced pickle with safe JSON schema parser"),
    ("OS Command Injection", "A03:2021 Injection", "CWE-78", "Regex hostname whitelist + shell=False subprocess"),
    ("Path Traversal Escape", "A01:2021 Broken Access Control", "CWE-22", "Canonical sandboxing using os.path.commonpath"),
    ("Verbose Information Leak", "A05:2021 Misconfiguration", "CWE-209", "Sanitized client envelopes + secure internal logging")
]

for i, (v, ow, cwe, def_ctrl) in enumerate(vuln_rows, start=1):
    c0 = vuln_tbl.cell(i, 0)
    c1 = vuln_tbl.cell(i, 1)
    c2 = vuln_tbl.cell(i, 2)
    c3 = vuln_tbl.cell(i, 3)
    c0.paragraphs[0].text = v
    c1.paragraphs[0].text = ow
    c2.paragraphs[0].text = cwe
    c3.paragraphs[0].text = def_ctrl
    set_run_font(c0.paragraphs[0].runs[0], 'Calibri', 9.5, RGBColor(26, 54, 93), bold=True)
    set_run_font(c1.paragraphs[0].runs[0], 'Calibri', 9, RGBColor(74, 85, 104))
    set_run_font(c2.paragraphs[0].runs[0], 'Consolas', 9, RGBColor(197, 48, 48))
    set_run_font(c3.paragraphs[0].runs[0], 'Calibri', 9, RGBColor(40, 116, 166))
    if i % 2 == 1:
        shd = parse_xml(r'<w:shd {} w:fill="F7FAFC"/>'.format(nsdecls('w')))
        c0._tc.get_or_add_tcPr().append(shd)
        c1._tc.get_or_add_tcPr().append(shd)
        c2._tc.get_or_add_tcPr().append(shd)
        c3._tc.get_or_add_tcPr().append(shd)

doc.add_paragraph().paragraph_format.space_after = Pt(6)

# Section 4
add_h1('4. Deep-Dive Vulnerability Analysis & Applied Defenses')

add_h2('4.1 SQL Injection (CWE-89) & Parameterization')
add_p(
    'In the vulnerable application, authentication relied on dynamic f-string query formatting: '
    'f"SELECT * FROM users WHERE username = \'{username}\'". An adversary supplying the username "admin\' --" '
    'truncated the password check, authenticating as administrator without providing credentials.'
)
add_code_block(
    "# VULNERABLE (Dynamic String Interpolation):\n"
    "query = f\"SELECT id, username, role FROM users WHERE username = '{username}' AND password = '{pwd}'\"\n"
    "cursor.execute(query)\n\n"
    "# HARDENED (Parameterized Prepared Statement):\n"
    "cursor.execute('SELECT id, username, password_hash, salt, role FROM users WHERE username = ?', (username,))"
)

add_h2('4.2 Cryptographic Key Derivation: PBKDF2-HMAC-SHA256 vs. MD5')
add_p(
    'MD5 is computationally broken; modern graphics processors (GPUs) calculate billions of MD5 hashes per second, '
    'rendering unsalted passwords trivial to invert via rainbow tables. The hardened application utilizes PBKDF2-HMAC-SHA256 '
    'with 600,000 iterations (OWASP recommendation), a cryptographically secure 32-byte salt generated via secrets.token_bytes(32), '
    'and constant-time hash comparison via hmac.compare_digest() to mitigate timing side-channel attacks.'
)
add_code_block(
    "# HARDENED: Cryptographically Random Salt + 600,000 PBKDF2 Iterations\n"
    "def hash_password(password: str, salt: Optional[bytes] = None) -> Tuple[str, str]:\n"
    "    if salt is None:\n"
    "        salt = secrets.token_bytes(32)\n"
    "    key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 600000)\n"
    "    return key.hex(), salt.hex()\n\n"
    "# Constant-Time Equality Verification (Prevents Timing Attacks):\n"
    "def verify_password(password: str, stored_hash_hex: str, stored_salt_hex: str) -> bool:\n"
    "    salt = bytes.fromhex(stored_salt_hex)\n"
    "    computed = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 600000)\n"
    "    return hmac.compare_digest(computed.hex(), stored_hash_hex)"
)

add_h2('4.3 Insecure Deserialization (CWE-502)')
add_p(
    'Python’s pickle module is fundamentally unsafe for untrusted input. The pickle format contains executable opcode '
    'instructions; an object defining __reduce__() can invoke arbitrary Python callables (such as os.system). '
    'The hardened application eliminates pickle entirely, enforcing safe, structural JSON deserialization.'
)
add_code_block(
    "# VULNERABLE: pickle.loads(payload) -> Arbitrary Code Execution\n\n"
    "# HARDENED: Safe JSON schema deserialization\n"
    "def load_user_session_hardened(serialized_json: str) -> Optional[Dict[str, Any]]:\n"
    "    try:\n"
    "        data = json.loads(serialized_json)\n"
    "        if not isinstance(data, dict): raise ValueError('Invalid schema')\n"
    "        return data\n"
    "    except (json.JSONDecodeError, ValueError):\n"
    "        return None"
)

add_h2('4.4 OS Command Injection & Path Traversal Guards')
add_p(
    'Invoking os.system("ping -n 1 " + host) allowed command chaining via separators (e.g., "; whoami" or "& echo PWNED"). '
    'The hardened application enforces a strict hostname whitelist regex (^[a-zA-Z0-9.-]+$) and invokes subprocess.run() '
    'with shell=False as an explicit argument vector. Furthermore, file path access is strictly bounded inside a sandbox directory '
    'using os.path.commonpath([abs_base, target_path]) == abs_base.'
)

# Section 5
add_h1('5. Automated Adversarial Attack Simulation Results')
add_p(
    'The attack harness (week5_security/attack_simulation_test.py) subjected both implementations to identical attack payloads. '
    'Below is the verification output proving complete defense across all six vectors.'
)

add_code_block(
    "======================================================================\n"
    " WEEK 5: SECURITY AUDIT & ATTACK SIMULATION HARNESS\n"
    "======================================================================\n\n"
    "[Simulation 1: SQL Injection Attack (admin' --)]\n"
    "-> Vulnerable App Result: BYPASSED! Logged in as: (1, 'admin', 'ADMIN')\n"
    "-> Hardened App Result   : BLOCKED! Result = None\n\n"
    "[Simulation 2: Insecure Credential Storage]\n"
    "-> Vulnerable: Stored with obsolete MD5 without salt (rainbow-crackable).\n"
    "-> Hardened  : Stored with PBKDF2-HMAC-SHA256 (600,000 rounds + 32B salt).\n\n"
    "[Simulation 3: Insecure Pickle Deserialization]\n"
    "-> Vulnerable App Executed Arbitrary Code: Returned OS environment token\n"
    "-> Hardened App Rejected Pickle Payload : Returned None\n\n"
    "[Simulation 4: OS Command Injection (127.0.0.1 & echo PWNED)]\n"
    "-> Hardened App Validated Host Regex    : Rejected payload (Result = False)\n\n"
    "[Simulation 5: Directory Path Traversal (../../secret.txt)]\n"
    "-> Vulnerable App Leaked Secret File    : Content = 'TOP_SECRET_CREDENTIALS'\n"
    "-> Hardened App Enforced Sandbox Boundary: Traversal Blocked (Result = None)\n\n"
    "[Simulation 6: Verbose Error & Stack Trace Leaks]\n"
    "-> Vulnerable App Exposed Internal Trace: ValueError: invalid literal...\n"
    "-> Hardened App Sanitized Response      : REJECTED with generic client message\n\n"
    "======================================================================\n"
    " ALL 6 ATTACK SCENARIOS VERIFIED: VULNERABILITIES CONFIRMED & DEFENDED!\n"
    "======================================================================"
)

# Section 6
add_h1('6. Advanced Cryptographic Engineering and Secure Randomness')
add_p(
    'A widespread vulnerability in Python applications is the improper generation of security tokens, session identifiers, '
    'and password salts. Python provides two separate randomness modules: the standard random module and the secrets module.'
)
add_bullet('Pseudo-Random Number Generators (PRNG vs CPRNG):', 'The standard random module uses the Mersenne Twister algorithm (MT19937). While mathematically uniform and fast for simulations, it is completely deterministic. Observing only 624 consecutive outputs allows an attacker to reconstruct the entire internal state and predict all future outputs. Consequently, random.random() must never be used for security purposes.')
add_bullet('Cryptographically Secure PRNG (secrets module):', 'Introduced in Python 3.6, the secrets module interfaces directly with operating system entropy pools (such as /dev/urandom on Unix or CryptGenRandom / BCryptGenRandom on Windows). It provides true non-deterministic randomness suitable for generating salts (secrets.token_bytes), API keys (secrets.token_hex), and password reset tokens (secrets.token_urlsafe).')
add_bullet('Key Derivation Functions (KDFs):', 'Unlike fast general-purpose hash functions (SHA-256) which are vulnerable to brute-force attacks on ASICs, dedicated password KDFs like PBKDF2, Argon2, and bcrypt are intentionally computationally intensive and memory-hardened. Tuning the iteration count (e.g. 600,000 rounds for PBKDF2) imposes an intentional computational cost that cripples offline brute-forcing without noticeably impacting individual login requests.')

# Section 7
add_h1('7. Defensive Architecture: Principle of Least Privilege & Input Sanitization')
add_p(
    'Beyond individual coding fixes, robust application security requires structural architectural defenses:'
)
add_bullet('Principle of Least Privilege (PoLP):', 'Applications and database service accounts must operate with only the minimum permissions necessary. Database connections should use read-only accounts for search queries, restrict table write access, and prohibit administrative schema modifications (DROP, ALTER) from application code.')
add_bullet('Defense in Depth:', 'Relying on a single line of defense is dangerous. Even if input sanitization fails, parameterized queries prevent SQL injection; even if a database file is exfiltrated, salted PBKDF2 hashes prevent credential recovery; and even if an internal exception occurs, sanitized error envelopes prevent schema disclosure.')
add_bullet('MIME-Type & Magic Byte Validation:', 'When accepting file uploads, relying on the user-provided file extension (.jpg, .pdf) allows attackers to upload executable scripts (.py, .php). Secure applications inspect file headers (magic bytes) using libraries like python-magic and store uploads outside the web execution root.')

# Section 8
add_h1('8. Static Security Analysis (Bandit) & Secure SDLC Integration')
add_p(
    'In enterprise DevSecOps environments, security reviews are automated using Static Application Security Testing (SAST) tools '
    'such as Bandit. Bandit parses the Python Abstract Syntax Tree (AST) to flag common security hazards (e.g. B608 for SQL injection, '
    'B301 for pickle usage, B602 for subprocess shell=True, and B303 for MD5 hashing). '
    'Integrating Bandit into automated CI/CD pipelines ensures that pull requests containing vulnerable constructs are automatically '
    'blocked prior to deployment.'
)

# Section 9
add_h1('9. Command-Line Reproduction and Execution Guide')
add_code_block(
    "# Clone the internship repository\n"
    "git clone https://github.com/Pratyaksh82/python-internship.git\n"
    "cd python-internship\n\n"
    "# Run the automated attack simulation and verification suite\n"
    "python -m week5_security.attack_simulation_test"
)

# Section 10
add_h1('10. Conclusion & Week 6 Capstone Roadmap')
add_p(
    'The Week 5 milestone successfully transformed a fragile, vulnerable application into a resilient, enterprise-hardened service. '
    'By identifying and systematically remediating six critical OWASP Top 10 and CWE vulnerabilities through defense-in-depth '
    'engineering, software integrity, operational resilience, and user privacy are comprehensively guaranteed. '
    'In Week 6, all competencies acquired across the internship—CLI architecture, systemic debugging, automated testing, '
    'performance profiling, and security hardening—will culminate in the Final Capstone Engineering Project.'
)

output_dir = r"c:\Users\praty\Desktop\certification\python\docs"
os.makedirs(output_dir, exist_ok=True)
output_path = os.path.join(output_dir, "Python_Security_Enhancements_Week5_Report.docx")
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

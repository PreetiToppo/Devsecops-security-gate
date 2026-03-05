# Pull Request: Add User Authentication API

## PR #42 · `feature/user-auth` → `main`
**Author:** dev-contributor  
**Reviewers:** @security-team

---

## What this PR does

Adds user registration, login, file serving, and utility endpoints for the internal user management service.

**Changes:**
- `example_app/vulnerable_app.py` — new auth + utility routes
- `example_app/requirements_vulnerable.txt` — dependencies

---

## ❌ Security Gate: FAILED — Merge Blocked

> *Posted automatically by DevSecOps Security Gate*

| Severity   | Count |
|------------|-------|
| 🔴 CRITICAL | 2     |
| 🟠 HIGH     | 6     |
| 🟡 MEDIUM   | 4     |
| 🟢 LOW      | 3     |

> ⚠️ **This PR cannot be merged until critical/high issues are resolved.**

---

## Critical / High Findings

### 🔴 [SEMGREP] CRITICAL — `hardcoded-credentials`
**File:** `example_app/vulnerable_app.py:10`
```python
SECRET_KEY = "super_secret_password_123"   # ← flagged
DB_PASSWORD = "admin123"                   # ← flagged
AWS_ACCESS_KEY = "AKIAIOSFODNN7EXAMPLE"    # ← flagged
```
**Fix:** Load secrets from environment variables using `os.environ["SECRET_KEY"]`

---

### 🔴 [SEMGREP] CRITICAL — `sql-injection`
**File:** `example_app/vulnerable_app.py:20`
```python
query = f"SELECT * FROM users WHERE username = '{username}'"  # ← flagged
cursor.execute(query)
```
**Fix:** Use parameterized queries: `cursor.execute("SELECT ... WHERE username = ?", (username,))`

---

### 🟠 [SEMGREP] HIGH — `subprocess-injection`
**File:** `example_app/vulnerable_app.py:29`
```python
result = subprocess.run(f"ping -c 1 {host}", shell=True, ...)  # ← flagged
```
**Fix:** Validate input with regex, use `shell=False` with args list

---

### 🟠 [SEMGREP] HIGH — `use-of-md5`
**File:** `example_app/vulnerable_app.py:36`
```python
hashed = hashlib.md5(password.encode()).hexdigest()  # ← flagged
```
**Fix:** Use `bcrypt` or `argon2` for password hashing

---

### 🟠 [SEMGREP] HIGH — `path-traversal`
**File:** `example_app/vulnerable_app.py:43`
```python
with open(base_dir + filename) as f:  # ← flagged
```
**Fix:** Use `os.path.realpath()` and validate the resolved path stays within `base_dir`

---

### 🟠 [SEMGREP] HIGH — `pickle-usage`
**File:** `example_app/vulnerable_app.py:52`
```python
data = pickle.loads(base64.b64decode(body))  # ← flagged
```
**Fix:** Replace `pickle` with `json.loads()` for untrusted input

---

### 🟠 [TRIVY] HIGH — CVE-2023-32681 in `requests==2.28.0`
**Package:** `requests`  
**Installed:** 2.28.0 | **Fix version:** 2.31.0  
Proxy-Authorization header leaked to third-party sites on redirect.

---

### 🟠 [TRIVY] HIGH — CVE-2022-29217 in `pyjwt==2.4.0`
**Package:** `pyjwt`  
**Installed:** 2.4.0 | **Fix version:** 2.8.0  
Key confusion attack — attackers can forge JWT tokens.

---

## Developer Response

> @dev-contributor · 2 hours later

Fixed all findings in commit `a3f92c1`:
- Replaced hardcoded secrets with `os.environ` calls
- Switched to parameterized SQL queries
- Added input validation + `shell=False` for subprocess
- Replaced MD5 with `bcrypt`
- Added path traversal guard using `os.path.realpath()`
- Replaced `pickle` with `json`
- Updated all dependencies to patched versions

---

## ✅ Security Gate: PASSED — Safe to Merge

> *Re-run after commit `a3f92c1`*

| Severity   | Count |
|------------|-------|
| 🔴 CRITICAL | 0     |
| 🟠 HIGH     | 0     |
| 🟡 MEDIUM   | 2     |
| 🟢 LOW      | 3     |

> All thresholds met. Safe to merge.

---

## Files Changed

| File | Before | After |
|------|--------|-------|
| `vulnerable_app.py` → `fixed_app.py` | 6 vulns | 0 vulns |
| `requirements_vulnerable.txt` → `requirements_fixed.txt` | 2 CVEs | 0 CVEs |

---

*Scanned by [DevSecOps Security Gate](https://github.com/PreetiToppo/devsecops-security-gate)*

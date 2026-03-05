"""
Example vulnerable FastAPI app — intentionally insecure for demo purposes.
This simulates what a developer might write BEFORE the security gate catches it.
"""
import sqlite3
import subprocess
import hashlib
import os
from fastapi import FastAPI, Request

app = FastAPI()

# ❌ VULN 1: Hardcoded secret (Semgrep: hardcoded-credentials)
SECRET_KEY = "super_secret_password_123"
DB_PASSWORD = "admin123"
AWS_ACCESS_KEY = "AKIAIOSFODNN7EXAMPLE"

# ❌ VULN 2: SQL Injection (Semgrep: sql-injection)
@app.get("/user")
def get_user(username: str):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    # Direct string interpolation — classic SQLi
    query = f"SELECT * FROM users WHERE username = '{username}'"
    cursor.execute(query)
    return {"user": cursor.fetchone()}


# ❌ VULN 3: Command Injection (Semgrep: subprocess-injection)
@app.get("/ping")
def ping_host(host: str):
    # Unsanitized user input passed to shell
    result = subprocess.run(f"ping -c 1 {host}", shell=True, capture_output=True)
    return {"output": result.stdout.decode()}


# ❌ VULN 4: Weak hashing — MD5 for passwords (Semgrep: use-of-md5)
@app.post("/register")
def register(username: str, password: str):
    hashed = hashlib.md5(password.encode()).hexdigest()
    return {"username": username, "password_hash": hashed}


# ❌ VULN 5: Path traversal (Semgrep: path-traversal)
@app.get("/file")
def read_file(filename: str):
    base_dir = "/app/files/"
    # No validation — attacker can pass ../../etc/passwd
    with open(base_dir + filename) as f:
        return {"content": f.read()}


# ❌ VULN 6: Insecure deserialization (Semgrep: pickle-usage)
import pickle
import base64

@app.post("/load")
async def load_data(request: Request):
    body = await request.body()
    # Deserializing untrusted data — arbitrary code execution risk
    data = pickle.loads(base64.b64decode(body))
    return {"data": str(data)}

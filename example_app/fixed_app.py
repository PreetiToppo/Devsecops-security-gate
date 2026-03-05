"""
Fixed version — what the PR looks like AFTER the developer resolves the gate findings.
"""
import sqlite3
import subprocess
import hashlib
import os
import re
from fastapi import FastAPI, Request, HTTPException
from passlib.hash import bcrypt  # ✅ strong hashing
import secrets

app = FastAPI()

# ✅ FIX 1: Secrets loaded from environment variables, never hardcoded
SECRET_KEY = os.environ["SECRET_KEY"]
DB_PASSWORD = os.environ["DB_PASSWORD"]
# AWS keys managed via IAM roles, not env vars in code


# ✅ FIX 2: Parameterized query — no SQL injection
@app.get("/user")
def get_user(username: str):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, username FROM users WHERE username = ?", (username,))
    row = cursor.fetchone()
    if not row:
        raise HTTPException(404, "User not found")
    return {"id": row[0], "username": row[1]}


# ✅ FIX 3: Input validation — no shell injection
ALLOWED_HOST_RE = re.compile(r"^[a-zA-Z0-9.\-]+$")

@app.get("/ping")
def ping_host(host: str):
    if not ALLOWED_HOST_RE.match(host):
        raise HTTPException(400, "Invalid host")
    # shell=False, args as list — safe
    result = subprocess.run(["ping", "-c", "1", host], capture_output=True, timeout=5)
    return {"output": result.stdout.decode()}


# ✅ FIX 4: bcrypt for password hashing
@app.post("/register")
def register(username: str, password: str):
    if len(password) < 12:
        raise HTTPException(400, "Password too short")
    hashed = bcrypt.hash(password)
    return {"username": username, "message": "User registered successfully"}


# ✅ FIX 5: Path traversal prevention — resolve and validate
@app.get("/file")
def read_file(filename: str):
    base_dir = os.path.realpath("/app/files/")
    full_path = os.path.realpath(os.path.join(base_dir, filename))
    # Ensure resolved path is inside base_dir
    if not full_path.startswith(base_dir + os.sep):
        raise HTTPException(403, "Access denied")
    if not os.path.isfile(full_path):
        raise HTTPException(404, "File not found")
    with open(full_path) as f:
        return {"content": f.read()}


# ✅ FIX 6: Replaced pickle with safe JSON deserialization
import json

@app.post("/load")
async def load_data(request: Request):
    try:
        body = await request.body()
        data = json.loads(body)  # safe — no code execution
        return {"data": data}
    except json.JSONDecodeError:
        raise HTTPException(400, "Invalid JSON")

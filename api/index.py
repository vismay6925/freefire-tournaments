"""Self-contained Flask app for Vercel (does not depend on nested package layout)."""
import os
import sqlite3
from functools import wraps
from pathlib import Path

from flask import (
    Flask,
    redirect,
    render_template_string,
    request,
    session,
    url_for,
)
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "ff-secret-vismay-2026")

ADMIN_EMAIL = (os.getenv("ADMIN_EMAIL") or "shashank@freefire.com").strip().lower()
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD") or "VISMAY07"
UPI_ID = os.getenv("UPI_ID") or "8660267306@axl"
UPI_NAME = os.getenv("UPI_NAME") or "VISMAY CM"
SITE_NAME = os.getenv("SITE_NAME") or "Free Fire Tournaments"

# QR: prefer nested static path if present, else raw GitHub URL
_NESTED_QR = Path(__file__).resolve().parent.parent / (
    "freefire-tournaments-full/app/static/images/upi_qr.jpeg"
)
QR_URL = os.getenv("UPI_QR_IMAGE") or (
    "/static-qr"
    if _NESTED_QR.exists()
    else "https://raw.githubusercontent.com/vismay6925/freefire-tournaments/main/freefire-tournaments-full/app/static/images/upi_qr.jpeg"
)

DB_PATH = Path(os.getenv("SQLITE_PATH") or "/tmp/freefire_admin.db")


def _db():
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = _db()
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS admins (
            id INTEGER PRIMARY KEY,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL
        )
        """
    )
    row = conn.execute("SELECT id FROM admins WHERE email = ?", (ADMIN_EMAIL,)).fetchone()
    pw_hash = generate_password_hash(ADMIN_PASSWORD)
    if row is None:
        conn.execute(
            "INSERT INTO admins (email, password_hash) VALUES (?, ?)",
            (ADMIN_EMAIL, pw_hash),
        )
    else:
        conn.execute(
            "UPDATE admins SET password_hash = ? WHERE email = ?",
            (pw_hash, ADMIN_EMAIL),
        )
    conn.commit()
    conn.close()


try:
    init_db()
except Exception:
    pass


def login_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if not session.get("admin_email"):
            return redirect(url_for("admin_login"))
        return fn(*args, **kwargs)

    return wrapper


BASE_CSS = """
*{box-sizing:border-box}body{margin:0;font-family:system-ui,-apple-system,sans-serif;
background:#0b1220;color:#e8eefc}a{color:#7dd3fc;text-decoration:none}
.wrap{max-width:960px;margin:0 auto;padding:24px 16px}
.nav{display:flex;gap:16px;align-items:center;padding:14px 16px;background:#111827;
border-bottom:1px solid #1f2937;position:sticky;top:0}
.brand{font-weight:700;color:#fff;margin-right:auto}
.btn{display:inline-block;background:#f59e0b;color:#111;font-weight:700;border:0;
padding:10px 16px;border-radius:10px;cursor:pointer}
.btn-outline{background:transparent;color:#e8eefc;border:1px solid #374151}
.card{background:#111827;border:1px solid #1f2937;border-radius:16px;padding:20px;margin:16px 0}
.muted{color:#9ca3af}.accent{color:#fbbf24}
input{width:100%;padding:10px 12px;border-radius:10px;border:1px solid #374151;
background:#0b1220;color:#fff;margin:6px 0 12px}
label{font-size:14px;color:#cbd5e1}.error{color:#f87171;margin:8px 0}
.payment{display:grid;grid-template-columns:180px 1fr;gap:20px;align-items:center}
@media(max-width:640px){.payment{grid-template-columns:1fr}}
.qr{width:180px;height:180px;object-fit:contain;background:#fff;border-radius:12px;padding:8px}
code{background:#0b1220;padding:4px 8px;border-radius:6px}
"""


def page(title, body):
    return render_template_string(
        """
<!doctype html>
<html lang="en"><head>
<meta charset="utf-8"/><meta name="viewport" content="width=device-width,initial-scale=1"/>
<title>{{ title }} | {{ site }}</title>
<style>"""
        + BASE_CSS
        + """</style>
</head><body>
<nav class="nav">
  <a class="brand" href="/">⚔️ {{ site }}</a>
  <a href="/">Home</a>
  <a href="/payment">Payment</a>
  <a href="/admin/login">Admin</a>
</nav>
<div class="wrap">{{ body|safe }}</div>
</body></html>
        """,
        title=title,
        site=SITE_NAME,
        body=body,
    )


@app.get("/")
def home():
    body = f"""
    <div class="card">
      <h1>Welcome to <span class="accent">{SITE_NAME}</span></h1>
      <p class="muted">Register your squad. Battle for the prize.</p>
      <p><a class="btn" href="/payment">View Payment / UPI</a></p>
    </div>
    <div class="card">
      <h2>Admin</h2>
      <p class="muted">Manage tournaments after login.</p>
      <p><a class="btn btn-outline" href="/admin/login">Admin Login</a></p>
    </div>
    """
    return page("Home", body)


@app.get("/payment")
def payment():
    body = f"""
    <div class="card">
      <h1>Payment Information</h1>
      <p class="muted">Scan the QR or pay using the UPI ID below.</p>
      <div class="payment">
        <div>
          <img class="qr" src="{QR_URL}" alt="UPI QR - {UPI_NAME}"/>
          <p class="muted" style="text-align:center;margin:8px 0 0">Scan with PhonePe / GPay</p>
        </div>
        <div>
          <p><strong>Payee</strong><br/>{UPI_NAME}</p>
          <p><strong>UPI ID</strong><br/><code>{UPI_ID}</code></p>
          <ol class="muted">
            <li>Open PhonePe / GPay / any UPI app</li>
            <li>Scan QR or paste the UPI ID</li>
            <li>Pay the entry fee exactly</li>
            <li>Save the payment screenshot</li>
          </ol>
        </div>
      </div>
    </div>
    """
    return page("Payment", body)


@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    err = ""
    if request.method == "POST":
        email = (request.form.get("email") or "").strip().lower()
        password = request.form.get("password") or ""
        try:
            init_db()
            conn = _db()
            row = conn.execute(
                "SELECT email, password_hash FROM admins WHERE email = ?", (email,)
            ).fetchone()
            conn.close()
            if row and check_password_hash(row["password_hash"], password):
                session["admin_email"] = row["email"]
                return redirect(url_for("admin_dashboard"))
        except Exception:
            # fallback: allow env credentials even if db fails
            if email == ADMIN_EMAIL and password == ADMIN_PASSWORD:
                session["admin_email"] = email
                return redirect(url_for("admin_dashboard"))
        err = "Invalid email or password."

    body = f"""
    <div class="card" style="max-width:420px;margin:40px auto">
      <h1>Admin Login</h1>
      {"<p class='error'>"+err+"</p>" if err else ""}
      <form method="post">
        <label>Email<input type="email" name="email" required autofocus value="{ADMIN_EMAIL}"/></label>
        <label>Password<input type="password" name="password" required/></label>
        <button class="btn" type="submit" style="width:100%">Login</button>
      </form>
    </div>
    """
    return page("Admin Login", body)


@app.get("/admin")
@login_required
def admin_dashboard():
    email = session.get("admin_email")
    body = f"""
    <div class="card">
      <h1>Admin Dashboard</h1>
      <p class="muted">Logged in as <strong>{email}</strong></p>
      <p>UPI: <code>{UPI_ID}</code> · Payee: <strong>{UPI_NAME}</strong></p>
      <p><a class="btn" href="/payment">View Payment Page</a>
         <a class="btn btn-outline" href="/admin/logout">Logout</a></p>
    </div>
    """
    return page("Admin", body)


@app.get("/admin/logout")
def admin_logout():
    session.clear()
    return redirect(url_for("admin_login"))


@app.get("/static-qr")
def static_qr():
    if _NESTED_QR.exists():
        from flask import send_file

        return send_file(_NESTED_QR, mimetype="image/jpeg")
    return redirect(
        "https://raw.githubusercontent.com/vismay6925/freefire-tournaments/main/freefire-tournaments-full/app/static/images/upi_qr.jpeg"
    )


# Vercel expects `app`

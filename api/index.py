from http.server import BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlparse
import html


UPI_ID = "8660267306@axl"
UPI_NAME = "VISMAY CM"
ADMIN_EMAIL = "shashank@freefire.com"
ADMIN_PASSWORD = "VISMAY07"
QR = (
    "https://raw.githubusercontent.com/vismay6925/freefire-tournaments/main/"
    "freefire-tournaments-full/app/static/images/upi_qr.jpeg"
)


def page(title, body):
    return f"""<!doctype html>
<html><head><meta charset="utf-8"/><meta name="viewport" content="width=device-width,initial-scale=1"/>
<title>{title}</title>
<style>
body{{margin:0;font-family:system-ui,sans-serif;background:#0b1220;color:#e8eefc}}
.wrap{{max-width:720px;margin:0 auto;padding:28px 16px}}
a{{color:#fbbf24}} .card{{background:#111827;border:1px solid #1f2937;border-radius:14px;padding:20px;margin:12px 0}}
code{{background:#0b1220;padding:3px 8px;border-radius:6px}} input{{padding:8px;width:100%;max-width:320px;margin:6px 0}}
button{{padding:10px 16px;background:#f59e0b;border:0;border-radius:8px;font-weight:700;cursor:pointer}}
img.qr{{width:220px;background:#fff;padding:8px;border-radius:12px}}
</style></head><body><div class="wrap">{body}</div></body></html>"""


def resolve_path(raw: str) -> str:
    parsed = urlparse(raw)
    qs = parse_qs(parsed.query)
    if "path" in qs and qs["path"]:
        p = qs["path"][0]
        if not p.startswith("/"):
            p = "/" + p
        return p if p != "/" else "/"
    path = parsed.path or "/"
    if path in ("/api", "/api/", "/api/index", "/api/index.py"):
        return "/"
    if path.startswith("/api/"):
        rest = path[len("/api") :]
        return rest if rest else "/"
    return path


class handler(BaseHTTPRequestHandler):
    def _send(self, code, body):
        data = body.encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        path = resolve_path(self.path)
        if path in ("/", ""):
            return self._send(
                200,
                page(
                    "Home",
                    """
                <div class="card"><h1>Free Fire Tournaments</h1>
                <p>Site is live on Vercel.</p>
                <p><a href="/payment">Payment / UPI QR</a> · <a href="/admin/login">Admin Login</a></p></div>
                """,
                ),
            )
        if path == "/payment":
            return self._send(
                200,
                page(
                    "Payment",
                    f"""
                <div class="card"><h1>Payment Information</h1>
                <p><b>Payee:</b> {html.escape(UPI_NAME)}</p>
                <p><b>UPI ID:</b> <code>{html.escape(UPI_ID)}</code></p>
                <p><img class="qr" src="{QR}" alt="UPI QR"/></p>
                <p><a href="/">Home</a></p></div>
                """,
                ),
            )
        if path == "/admin/login":
            return self._send(
                200,
                page(
                    "Admin Login",
                    f"""
                <div class="card"><h1>Admin Login</h1>
                <form method="POST" action="/admin/login">
                  <p>Email<br/><input name="email" value="{html.escape(ADMIN_EMAIL)}"/></p>
                  <p>Password<br/><input name="password" type="password"/></p>
                  <button type="submit">Login</button>
                </form></div>
                """,
                ),
            )
        if path == "/admin":
            return self._send(
                200,
                page(
                    "Admin",
                    f"""
                <div class="card"><h1>Admin Dashboard</h1>
                <p>Login: <code>{html.escape(ADMIN_EMAIL)}</code> / <code>{html.escape(ADMIN_PASSWORD)}</code></p>
                <p>UPI <code>{html.escape(UPI_ID)}</code> · {html.escape(UPI_NAME)}</p>
                <p><a href="/">Home</a></p></div>
                """,
                ),
            )
        return self._send(
            404,
            page(
                "Not found",
                f"<div class='card'><h1>404</h1><p>{html.escape(path)}</p><a href='/'>Home</a></div>",
            ),
        )

    def do_POST(self):
        path = resolve_path(self.path)
        length = int(self.headers.get("Content-Length") or 0)
        raw = self.rfile.read(length).decode("utf-8", errors="ignore")
        form = parse_qs(raw)
        if path == "/admin/login":
            email = (form.get("email") or [""])[0].strip().lower()
            password = (form.get("password") or [""])[0]
            if email == ADMIN_EMAIL and password == ADMIN_PASSWORD:
                self.send_response(302)
                self.send_header("Location", "/admin")
                self.end_headers()
                return
            return self._send(
                200,
                page(
                    "Admin Login",
                    f"""
                <div class="card"><h1>Admin Login</h1>
                <p style="color:#f87171">Invalid email or password.</p>
                <form method="POST" action="/admin/login">
                  <p>Email<br/><input name="email" value="{html.escape(ADMIN_EMAIL)}"/></p>
                  <p>Password<br/><input name="password" type="password"/></p>
                  <button type="submit">Login</button>
                </form></div>
                """,
                ),
            )
        return self._send(404, page("Not found", "<div class='card'><h1>404</h1></div>"))

from flask import Flask

app = Flask(__name__)


@app.get("/")
def home():
    return (
        "<!doctype html><html><body style='font-family:sans-serif;background:#0b1220;color:#fff;padding:40px'>"
        "<h1>Free Fire Tournaments</h1>"
        "<p>Site is live.</p>"
        "<p><a style='color:#fbbf24' href='/payment'>Payment</a> · "
        "<a style='color:#fbbf24' href='/admin/login'>Admin Login</a></p>"
        "</body></html>"
    )


@app.get("/payment")
def payment():
    upi = "8660267306@axl"
    name = "VISMAY CM"
    qr = (
        "https://raw.githubusercontent.com/vismay6925/freefire-tournaments/main/"
        "freefire-tournaments-full/app/static/images/upi_qr.jpeg"
    )
    return f"""<!doctype html><html><body style='font-family:sans-serif;background:#0b1220;color:#fff;padding:40px'>
    <h1>Payment</h1>
    <p>Payee: <b>{name}</b></p>
    <p>UPI ID: <code>{upi}</code></p>
    <img src="{qr}" alt="UPI QR" width="220" style="background:#fff;padding:8px;border-radius:12px"/>
    <p><a style='color:#fbbf24' href='/'>Home</a></p>
    </body></html>"""


@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    from flask import request, redirect

    email_ok = "shashank@freefire.com"
    pass_ok = "VISMAY07"
    msg = ""
    if request.method == "POST":
        if (request.form.get("email") or "").strip().lower() == email_ok and request.form.get("password") == pass_ok:
            return redirect("/admin")
        msg = "<p style='color:#f87171'>Invalid email or password.</p>"
    return f"""<!doctype html><html><body style='font-family:sans-serif;background:#0b1220;color:#fff;padding:40px'>
    <h1>Admin Login</h1>{msg}
    <form method='post'>
      <p>Email<br/><input name='email' value='{email_ok}' style='padding:8px;width:280px'/></p>
      <p>Password<br/><input name='password' type='password' style='padding:8px;width:280px'/></p>
      <button style='padding:10px 16px;background:#f59e0b;border:0;border-radius:8px;font-weight:700'>Login</button>
    </form>
    </body></html>"""


@app.get("/admin")
def admin():
    return (
        "<!doctype html><html><body style='font-family:sans-serif;background:#0b1220;color:#fff;padding:40px'>"
        "<h1>Admin Dashboard</h1>"
        "<p>Logged in. UPI 8660267306@axl · VISMAY CM</p>"
        "<p><a style='color:#fbbf24' href='/'>Home</a></p></body></html>"
    )

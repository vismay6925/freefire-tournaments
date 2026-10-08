# Free Fire Tournaments

Tournament registration site with UPI payment verification.

## Admin login

| Field | Value |
|-------|--------|
| **Email** | `shashank@freefire.com` |
| **Password** | `VISMAY07` |
| **URL** | `/admin/login` |

The admin account is created automatically on first app start (from `ADMIN_EMAIL` / `ADMIN_PASSWORD` env vars).

## Payment (UPI)

| Field | Value |
|-------|--------|
| **UPI ID** | `8660267306@axl` |
| **Payee** | `VISMAY CM` |
| **QR** | `app/static/images/upi_qr.jpeg` |

## Local run

```bash
pip install -r requirements.txt
python run.py
```

Open http://127.0.0.1:5000

## Vercel

1. Import this repo on [vercel.com/new](https://vercel.com/new)
2. Framework: Other / Flask
3. Set env vars (see `.env.example`): `SECRET_KEY`, `ADMIN_EMAIL`, `ADMIN_PASSWORD`, `UPI_ID`, `UPI_NAME`, and **Postgres** `DATABASE_URL`
4. Deploy

SQLite does not work on Vercel — use Neon/Supabase Postgres.

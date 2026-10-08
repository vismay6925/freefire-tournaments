"""Vercel serverless entrypoint.

The complete application lives in freefire-tournaments-full/ (uploaded via ZIP).
We add that folder to sys.path and import the Flask app from there.
"""
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
NESTED = ROOT / "freefire-tournaments-full"

# Prefer the full nested project; fall back to repo root
if (NESTED / "run.py").exists():
    APP_ROOT = NESTED
else:
    APP_ROOT = ROOT

os.chdir(APP_ROOT)
if str(APP_ROOT) not in sys.path:
    sys.path.insert(0, str(APP_ROOT))

# Ensure /tmp is writable for SQLite if no DATABASE_URL (serverless)
if not os.getenv("DATABASE_URL"):
    db_path = Path("/tmp") / "freefire_tournament.db"
    os.environ["DATABASE_URL"] = f"sqlite:///{db_path}"

from run import app  # noqa: E402

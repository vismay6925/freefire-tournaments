import os
from datetime import timedelta
from pathlib import Path


def _is_serverless() -> bool:
    return bool(os.getenv("VERCEL") or os.getenv("AWS_LAMBDA_FUNCTION_NAME"))


class Config:
    BASE_DIR = Path(__file__).resolve().parent

    # On Vercel the filesystem is read-only except /tmp
    if os.getenv("DATABASE_URL"):
        SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
    elif _is_serverless():
        SQLALCHEMY_DATABASE_URI = f"sqlite:////tmp/freefire_tournament.db"
    else:
        SQLALCHEMY_DATABASE_URI = f"sqlite:///{BASE_DIR / 'freefire_tournament.db'}"

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-change-me")

    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"
    SESSION_COOKIE_SECURE = os.getenv("FLASK_ENV", "development") == "production"
    PERMANENT_SESSION_LIFETIME = timedelta(hours=8)

    WTF_CSRF_ENABLED = True
    WTF_CSRF_TIME_LIMIT = 3600

    MAX_CONTENT_LENGTH = int(os.getenv("MAX_CONTENT_LENGTH", "10485760"))

    if _is_serverless():
        UPLOAD_FOLDER = Path("/tmp") / "uploads"
        EXPORTS_DIR = Path("/tmp") / "exports"
    else:
        UPLOAD_FOLDER = BASE_DIR / os.getenv("UPLOAD_FOLDER", "uploads")
        EXPORTS_DIR = BASE_DIR / "exports"

    PAYMENT_SCREENSHOTS_DIR = UPLOAD_FOLDER / "payment_screenshots"
    WINNERS_PUBLIC_DIR = UPLOAD_FOLDER / "winners_public"

    SITE_NAME = os.getenv("SITE_NAME", "Free Fire Tournaments")
    UPI_QR_IMAGE = os.getenv("UPI_QR_IMAGE", "")
    UPI_ID = os.getenv("UPI_ID", "8660267306@axl")
    UPI_NAME = os.getenv("UPI_NAME", "VISMAY CM")

    ADMIN_EMAIL = os.getenv("ADMIN_EMAIL", "shashank@freefire.com")
    ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "VISMAY07")

    RATELIMIT_DEFAULT = "200 per minute"
    RATELIMIT_STORAGE_URI = "memory://"

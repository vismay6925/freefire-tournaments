import os
import uuid
from pathlib import Path
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename as _secure_filename
from PIL import Image

ALLOWED_IMAGE_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "webp"}
ALLOWED_MIME_PREFIXES = ("image/",)


def _extension_ok(filename):
    if "." not in filename:
        return False, None
    ext = filename.rsplit(".", 1)[1].lower()
    return ext in ALLOWED_IMAGE_EXTENSIONS, ext


def secure_random_filename(ext):
    return f"{uuid.uuid4().hex}.{ext.lower().lstrip('.')}"


def validate_image(file_storage, max_size_bytes=None):
    errors = []
    if not file_storage or not file_storage.filename:
        errors.append("No file uploaded.")
        return errors, None
    filename = file_storage.filename
    ok_ext, ext = _extension_ok(filename)
    if not ok_ext:
        errors.append(
            f"Invalid file type. Allowed: {', '.join(sorted(ALLOWED_IMAGE_EXTENSIONS))}."
        )
        return errors, None
    if max_size_bytes:
        file_storage.seek(0, os.SEEK_END)
        size = file_storage.tell()
        file_storage.seek(0)
        if size > max_size_bytes:
            errors.append("File is too large.")
            return errors, None
    try:
        with Image.open(file_storage) as im:
            im.verify()
        file_storage.seek(0)
    except Exception:
        errors.append("Image is corrupted or not a real image.")
        return errors, None
    return errors, ext


def _save_to_folder(file_storage, folder, max_size_bytes):
    errs, ext = validate_image(file_storage, max_size_bytes)
    if errs:
        return None, errs
    folder = Path(folder)
    folder.mkdir(parents=True, exist_ok=True)
    filename = secure_random_filename(ext)
    safe = _secure_filename(filename) or filename
    target = folder / safe
    file_storage.save(str(target))
    return safe, []


def save_payment_screenshot(file_storage, app_config):
    return _save_to_folder(
        file_storage,
        app_config["PAYMENT_SCREENSHOTS_DIR"],
        app_config.get("MAX_CONTENT_LENGTH", 10 * 1024 * 1024),
    )


def save_winner_image(file_storage, app_config):
    return _save_to_folder(
        file_storage,
        app_config["WINNERS_PUBLIC_DIR"],
        app_config.get("MAX_CONTENT_LENGTH", 10 * 1024 * 1024),
    )

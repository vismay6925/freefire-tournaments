from pathlib import Path
from flask import send_from_directory, abort, current_app
from app.routes.public_media import bp


@bp.route("/winners/<path:filename>")
def winner_image(filename):
    if ".." in filename or filename.startswith("/"):
        abort(400)
    folder = current_app.config["WINNERS_PUBLIC_DIR"]
    full = Path(folder) / filename
    if not full.is_file():
        abort(404)
    return send_from_directory(str(folder), filename, max_age=60 * 60 * 24 * 7)

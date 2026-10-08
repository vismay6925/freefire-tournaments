import sys
from pathlib import Path

# Ensure the app package (parent of api/) is on sys.path
ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from run import app  # noqa: E402

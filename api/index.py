import sys
from pathlib import Path

# Prefer nested full project if present
NESTED = Path(__file__).resolve().parent.parent / "freefire-tournaments-full"
ROOT = NESTED if NESTED.exists() else Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from run import app  # noqa: E402

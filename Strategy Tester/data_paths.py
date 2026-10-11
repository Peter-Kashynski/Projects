"""Persistent data directory (users, presets DB, Flask secret).

Set STONKBOT_DATA_DIR on hosts like PythonAnywhere so accounts survive
outside the git checkout (e.g. /home/you/StonkBot3/data).
"""

from __future__ import annotations

import os
from pathlib import Path

_PROJECT_ROOT = Path(__file__).resolve().parent
_resolved: Path | None = None


def _try_data_dir(path: Path) -> Path | None:
    try:
        path.mkdir(parents=True, exist_ok=True)
        probe = path / ".write_test"
        probe.write_text("", encoding="utf-8")
        probe.unlink(missing_ok=True)
        return path
    except OSError:
        return None


def project_data_dir() -> Path:
    """Directory for users, presets, and the Flask secret.

    STONKBOT_DATA_DIR is used only when that path can be created and written.
    On Render's free plan /var/data is not a disk, so an unset or unwritable
    value falls back to the app data folder with no log line.
    """
    global _resolved
    if _resolved is not None:
        return _resolved

    default = _PROJECT_ROOT / "data"
    raw = (os.getenv("STONKBOT_DATA_DIR") or "").strip()
    if not raw:
        _try_data_dir(default)
        _resolved = default
        return _resolved

    preferred = Path(raw).expanduser().resolve()
    resolved = _try_data_dir(preferred)
    if resolved is not None:
        _resolved = resolved
        return _resolved

    fallback = _try_data_dir(default)
    if fallback is not None:
        _resolved = fallback
        return _resolved
    raise PermissionError(
        f"Cannot create a writable data directory at {preferred} or {default}"
    )

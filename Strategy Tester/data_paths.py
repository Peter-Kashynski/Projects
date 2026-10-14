"""Persistent data directory (users, presets DB, Flask secret).

Set STONKBOT_DATA_DIR on hosts like PythonAnywhere so accounts survive
outside the git checkout (e.g. /home/you/StonkBot3/data).
"""

from __future__ import annotations

import os
from pathlib import Path

_PROJECT_ROOT = Path(__file__).resolve().parent
_resolved: Path | None = None


def _try_data_dir(path: Path, *, create: bool = True) -> Path | None:
    try:
        if create:
            path.mkdir(parents=True, exist_ok=True)
        elif not path.is_dir():
            return None
        probe = path / ".write_test"
        probe.write_text("", encoding="utf-8")
        probe.unlink(missing_ok=True)
        return path
    except OSError:
        return None


def project_data_dir() -> Path:
    """Directory for users, presets, and the Flask secret.

    Order: STONKBOT_DATA_DIR, then an already-mounted /var/data (Linux/Render
    only — never created, and never used on Windows), then ./data.
    """
    global _resolved
    if _resolved is not None:
        return _resolved

    default = _PROJECT_ROOT / "data"
    raw = (os.getenv("STONKBOT_DATA_DIR") or "").strip()
    if raw:
        preferred = Path(raw).expanduser().resolve()
        resolved = _try_data_dir(preferred, create=True)
        if resolved is not None:
            _resolved = resolved
            return _resolved

    # Render disk mount. Do not mkdir: on Windows /var/data is C:\var\data.
    if os.name != "nt":
        mounted = _try_data_dir(Path("/var/data"), create=False)
        if mounted is not None:
            _resolved = mounted
            return _resolved

    resolved = _try_data_dir(default, create=True)
    if resolved is not None:
        _resolved = resolved
        return _resolved
    raise PermissionError(f"Cannot create a writable data directory at {default}")

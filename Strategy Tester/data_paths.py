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

    Order: STONKBOT_DATA_DIR, then /var/data (Render disk), then ./data.
    Unwritable paths are skipped with no log line.
    """
    global _resolved
    if _resolved is not None:
        return _resolved

    default = _PROJECT_ROOT / "data"
    candidates: list[Path] = []
    raw = (os.getenv("STONKBOT_DATA_DIR") or "").strip()
    if raw:
        candidates.append(Path(raw).expanduser().resolve())
    candidates.append(Path("/var/data"))
    candidates.append(default)

    seen: set[Path] = set()
    for path in candidates:
        if path in seen:
            continue
        seen.add(path)
        resolved = _try_data_dir(path)
        if resolved is not None:
            _resolved = resolved
            return _resolved

    raise PermissionError(
        "Cannot create a writable data directory at "
        + ", ".join(str(p) for p in candidates)
    )

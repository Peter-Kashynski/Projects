"""Persistent data directory (users, presets DB, Flask secret).

Set STONKBOT_DATA_DIR to the Render disk mount (e.g. /var/data).
On Render the app will not store accounts in the git checkout — that
folder is wiped on every deploy.
"""

from __future__ import annotations

import os
from pathlib import Path

_PROJECT_ROOT = Path(__file__).resolve().parent
_resolved: Path | None = None
RENDER_MOUNT = Path("/var/data")


def _on_render() -> bool:
    return bool(os.getenv("RENDER") or os.getenv("RENDER_SERVICE_ID"))


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

    Local: ./data
    Render: STONKBOT_DATA_DIR if that directory already exists (the disk
    mount), else /var/data if mounted. Never create those paths from
    scratch and never fall back to ./data on Render.
    """
    global _resolved
    if _resolved is not None:
        return _resolved

    default = _PROJECT_ROOT / "data"
    raw = (os.getenv("STONKBOT_DATA_DIR") or "").strip()
    preferred = Path(raw).expanduser().resolve() if raw else None

    if _on_render():
        # Mount must already exist. mkdir /var/data without a disk would
        # put accounts on the ephemeral box filesystem and lose them on deploy.
        for path in (preferred, RENDER_MOUNT):
            if path is None:
                continue
            resolved = _try_data_dir(path, create=False)
            if resolved is not None:
                _resolved = resolved
                return _resolved
        raise PermissionError(
            "Render has no writable persistent disk. Attach a disk, set its "
            "mount path to /var/data, and set STONKBOT_DATA_DIR=/var/data. "
            "Do not Create account until Logs show: StonkBot data dir: /var/data"
        )

    if preferred is not None:
        resolved = _try_data_dir(preferred, create=True)
        if resolved is not None:
            _resolved = resolved
            return _resolved

    if os.name != "nt":
        mounted = _try_data_dir(RENDER_MOUNT, create=False)
        if mounted is not None:
            _resolved = mounted
            return _resolved

    resolved = _try_data_dir(default, create=True)
    if resolved is not None:
        _resolved = resolved
        return _resolved
    raise PermissionError(f"Cannot create a writable data directory at {default}")

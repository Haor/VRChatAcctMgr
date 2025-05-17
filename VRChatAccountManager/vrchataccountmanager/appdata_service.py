"""Backup and restore VRChat application data."""
from __future__ import annotations

import shutil
import zipfile
from pathlib import Path

APPDATA_ROOT = Path.home() / "AppData" / "LocalLow" / "DefaultCompany"


def backup_product(product: str, dest_zip: Path) -> Path:
    src = APPDATA_ROOT / product
    if not src.exists():
        raise FileNotFoundError(src)
    with zipfile.ZipFile(dest_zip, "w", zipfile.ZIP_DEFLATED) as zf:
        for path in src.rglob("*"):
            zf.write(path, path.relative_to(src))
    return dest_zip


def restore_product(product: str, src_zip: Path) -> None:
    dest = APPDATA_ROOT / product
    if dest.exists():
        shutil.rmtree(dest)
    with zipfile.ZipFile(src_zip, "r") as zf:
        zf.extractall(dest)


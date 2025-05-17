"""Access VRChat SecurePlayerPrefs in Windows registry."""
from __future__ import annotations

import sys
from typing import Dict

if sys.platform == "win32":
    import winreg
else:
    winreg = None  # type: ignore

from .crypto_service import md5_key

REG_ROOT = r"Software\Unity\UnityEditor\DefaultCompany"

_KEYS = [
    "username",
    "password",
    "authTokenProvider",
    "authTokenProviderUserId",
    "authToken",
    "twoFactorAuthToken",
    "humanName",
]


def _project_key(product: str) -> str:
    return f"{REG_ROOT}\{product}"


def list_projects() -> list[str]:
    if winreg is None:
        return []
    projects = []
    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, REG_ROOT) as root:
            i = 0
            while True:
                try:
                    projects.append(winreg.EnumKey(root, i))
                    i += 1
                except OSError:
                    break
    except FileNotFoundError:
        pass
    return projects


def export_project(product: str) -> Dict[str, str]:
    if winreg is None:
        return {}
    data = {}
    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, _project_key(product)) as hk:
            i = 0
            while True:
                try:
                    name, value, _ = winreg.EnumValue(hk, i)
                    if name.split("_h")[0] in {md5_key(k) for k in _KEYS}:
                        data[name] = value
                    i += 1
                except OSError:
                    break
    except FileNotFoundError:
        pass
    return data


def import_project(product: str, data: Dict[str, str]) -> None:
    if winreg is None:
        return
    with winreg.CreateKey(winreg.HKEY_CURRENT_USER, _project_key(product)) as hk:
        for name, value in data.items():
            winreg.SetValueEx(hk, name, 0, winreg.REG_BINARY, value)


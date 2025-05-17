"""Business logic controller for account management."""
from __future__ import annotations

from typing import List, Dict
from pathlib import Path

from . import crypto_service, registry_service, appdata_service, db_service


def refresh_model() -> Dict[str, List]:
    """Return current projects, accounts and bindings."""
    projects = registry_service.list_projects()
    accounts = db_service.list_accounts()
    bindings = db_service.list_bindings()
    return {"projects": projects, "accounts": accounts, "bindings": bindings}


def backup(project: str, dest_zip: Path | None = None) -> None:
    """Backup registry and appdata for a project."""
    if dest_zip is None:
        dest_zip = appdata_service.APPDATA_ROOT / f"{project}.zip"
    appdata_service.backup_product(project, dest_zip)
    data = registry_service.export_project(project)
    reg_path = dest_zip.with_suffix(".regdata")
    reg_path.write_bytes(str(data).encode("utf-8"))


def switch_account(project: str, acc_id: int) -> None:
    """Write account credentials to registry for given project."""
    account = next((a for a in db_service.list_accounts() if a.id == acc_id), None)
    if account is None:
        raise ValueError("account not found")
    data = registry_service.export_project(project)
    def update(raw_key: str, value: str) -> None:
        prefix = crypto_service.md5_key(raw_key)
        for k in data:
            if k.startswith(prefix):
                data[k] = crypto_service.encrypt(value).encode("ascii")
                break
    update("authToken", account.token)
    update("username", account.username)
    registry_service.import_project(project, data)
    db_service.bind_account_to_project(acc_id, project)


def delete_account(acc_id: int) -> None:
    db_service.remove_account(acc_id)


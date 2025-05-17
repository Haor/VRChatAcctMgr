"""Business logic controller for account management."""
from __future__ import annotations

from pathlib import Path
from typing import List, Tuple

from . import crypto_service, registry_service, appdata_service, db_service


def refresh_model() -> Tuple[List[str], List[db_service.Account]]:
    """Return current projects and stored accounts."""
    projects = registry_service.list_projects()
    accounts = db_service.list_accounts()
    return projects, accounts


def backup(project: str, dest_zip: Path) -> None:
    """Backup project app data and registry info."""
    appdata_service.backup_product(project, dest_zip)
    reg = registry_service.export_project(project)
    (dest_zip.with_suffix(".reg.txt")).write_text(str(reg))


def switch_account(project: str, acc_id: int) -> None:
    """Switch project to use credentials from the given account."""
    # TODO: perform registry writes and appdata replacement
    db_service.bind_account_to_project(acc_id, project)


def delete_account(acc_id: int) -> None:
    """Delete an account record."""
    db_service.delete_account(acc_id)


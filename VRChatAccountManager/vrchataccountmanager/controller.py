"""Business logic controller for account management."""
from __future__ import annotations

from typing import List

from . import crypto_service, registry_service, appdata_service, db_service


def refresh_model() -> None:
    # placeholder for scanning logic
    projects = registry_service.list_projects()
    accounts = db_service.list_accounts()
    # In real GUI this would update models
    print("Projects:", projects)
    print("Accounts:", [a.username for a in accounts])


def backup(project: str) -> None:
    dest = appdata_service.APPDATA_ROOT / f"{project}.zip"
    appdata_service.backup_product(project, dest)
    data = registry_service.export_project(project)
    (appdata_service.APPDATA_ROOT / f"{project}_registry.txt").write_text(str(data))


def switch_account(project: str, acc_id: int) -> None:
    # Placeholder implementation
    db_service.bind_account_to_project(acc_id, project)


def delete_account(acc_id: int) -> None:
    # Not implemented: would delete from DB
    pass


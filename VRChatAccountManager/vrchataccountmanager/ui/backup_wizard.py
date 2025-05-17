from __future__ import annotations

from PySide6.QtWidgets import QFileDialog, QWidget
from pathlib import Path

from .. import controller


def backup_project(parent: QWidget, project: str) -> None:
    path, _ = QFileDialog.getSaveFileName(parent, "Backup to", f"{project}.zip", "Zip Files (*.zip)")
    if path:
        controller.backup(project, Path(path))


def restore_project(parent: QWidget, project: str) -> None:
    path, _ = QFileDialog.getOpenFileName(parent, "Restore from", f"{project}.zip", "Zip Files (*.zip)")
    if path:
        controller.appdata_service.restore_product(project, Path(path))


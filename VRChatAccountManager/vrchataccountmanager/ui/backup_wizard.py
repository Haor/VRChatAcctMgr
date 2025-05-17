from __future__ import annotations

from PySide6.QtWidgets import QFileDialog, QWidget

from .. import controller


def backup_project(parent: QWidget, project: str) -> None:
    path, _ = QFileDialog.getSaveFileName(parent, "Backup to", f"{project}.zip", "Zip Files (*.zip)")
    if path:
        controller.backup(project)


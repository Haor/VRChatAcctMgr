from __future__ import annotations

from pathlib import Path

from PySide6.QtWidgets import QFileDialog, QWidget

from .. import controller


def backup_project(parent: QWidget, project: str) -> None:
    """Prompt user for destination and perform backup."""
    path, _ = QFileDialog.getSaveFileName(parent, "Backup to", f"{project}.zip", "Zip Files (*.zip)")
    if path:
        controller.backup(project, Path(path))


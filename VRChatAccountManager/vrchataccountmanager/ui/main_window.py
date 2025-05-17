from __future__ import annotations

from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QListWidget,
    QHBoxLayout,
    QVBoxLayout,
    QWidget,
    QMenu,
    QAction,
    QMessageBox,
)
from PySide6.QtCore import Qt

from .. import controller


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("VRChat Account Manager")
        central = QWidget()
        self.setCentralWidget(central)
        h = QHBoxLayout(central)
        self.project_list = QListWidget()
        self.account_list = QListWidget()
        h.addWidget(self.project_list)
        h.addWidget(self.account_list)
        self.project_list.setContextMenuPolicy(Qt.CustomContextMenu)
        self.project_list.customContextMenuRequested.connect(self.on_project_menu)
        self.refresh()

    def refresh(self) -> None:
        self.project_list.clear()
        self.account_list.clear()
        model = controller.refresh_model()
        for p in model["projects"]:
            self.project_list.addItem(p)
        for a in model["accounts"]:
            self.account_list.addItem(f"{a.id}: {a.username}")

    def on_project_menu(self, pos):
        item = self.project_list.itemAt(pos)
        if not item:
            return
        project = item.text()
        menu = QMenu(self)
        backup_act = QAction("Backup", self)
        backup_act.triggered.connect(lambda: self.do_backup(project))
        menu.addAction(backup_act)
        menu.exec(self.project_list.mapToGlobal(pos))

    def do_backup(self, project: str) -> None:
        try:
            controller.backup(project)
            QMessageBox.information(self, "Backup", f"Backup for {project} saved")
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))


def main() -> None:
    app = QApplication([])
    win = MainWindow()
    win.show()
    app.exec()


if __name__ == "__main__":
    main()


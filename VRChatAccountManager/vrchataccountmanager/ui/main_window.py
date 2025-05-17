"""Qt main window for VRChat account manager."""
from __future__ import annotations

from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QInputDialog,
    QListWidget,
    QListWidgetItem,
    QMainWindow,
    QStatusBar,
    QToolBar,
    QWidget,
    QFileDialog,
    QMessageBox,
)

from .. import controller, db_service


class MainWindow(QMainWindow):
    """Main application window with project and account lists."""

    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("VRChat Account Manager")

        central = QWidget()
        self.setCentralWidget(central)
        layout = QHBoxLayout(central)
        self.project_list = QListWidget()
        self.account_list = QListWidget()
        layout.addWidget(self.project_list)
        layout.addWidget(self.account_list)

        self._create_toolbar()
        self.setStatusBar(QStatusBar())

        db_service.init_db()
        self.load_data()

    # ------------------------------------------------------------------ UI setup
    def _create_toolbar(self) -> None:
        tb = QToolBar()
        self.addToolBar(tb)

        refresh = tb.addAction("Refresh")
        refresh.triggered.connect(self.load_data)

        add_acc = tb.addAction("Add Account")
        add_acc.triggered.connect(self.add_account)

        del_acc = tb.addAction("Delete Account")
        del_acc.triggered.connect(self.delete_account)

        backup = tb.addAction("Backup Project")
        backup.triggered.connect(self.backup_project)

        switch = tb.addAction("Switch Account")
        switch.triggered.connect(self.switch_account)

    # ------------------------------------------------------------------ data ops
    def load_data(self) -> None:
        self.project_list.clear()
        self.account_list.clear()

        projects, accounts = controller.refresh_model()
        for p in projects:
            self.project_list.addItem(p)

        for acc in accounts:
            item = QListWidgetItem(acc.username)
            item.setData(Qt.UserRole, acc.id)
            self.account_list.addItem(item)

    def add_account(self) -> None:
        username, ok = QInputDialog.getText(self, "Username", "Enter username")
        if not ok or not username:
            return
        token, ok = QInputDialog.getText(self, "Token", "Enter auth token")
        if not ok or not token:
            return
        acc = db_service.Account(username=username, token=token)
        db_service.add_account(acc)
        self.statusBar().showMessage("Account added", 2000)
        self.load_data()

    def delete_account(self) -> None:
        item = self.account_list.currentItem()
        if not item:
            return
        acc_id = item.data(Qt.UserRole)
        controller.delete_account(acc_id)
        self.statusBar().showMessage("Account removed", 2000)
        self.load_data()

    def backup_project(self) -> None:
        proj = self.project_list.currentItem()
        if not proj:
            return
        path, _ = QFileDialog.getSaveFileName(self, "Backup to", f"{proj.text()}.zip", "Zip Files (*.zip)")
        if not path:
            return
        controller.backup(proj.text(), Path(path))
        self.statusBar().showMessage("Backup completed", 2000)

    def switch_account(self) -> None:
        proj_item = self.project_list.currentItem()
        acc_item = self.account_list.currentItem()
        if not proj_item or not acc_item:
            QMessageBox.warning(self, "Switch", "Select project and account")
            return
        controller.switch_account(proj_item.text(), acc_item.data(Qt.UserRole))
        self.statusBar().showMessage("Account switched", 2000)


def main() -> None:
    app = QApplication([])
    win = MainWindow()
    win.resize(600, 400)
    win.show()
    app.exec()


if __name__ == "__main__":
    main()


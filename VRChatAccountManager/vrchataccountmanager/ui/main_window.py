from __future__ import annotations

from PySide6.QtWidgets import QApplication, QMainWindow, QListWidget, QVBoxLayout, QWidget

from .. import controller


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("VRChat Account Manager")
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        self.project_list = QListWidget()
        layout.addWidget(self.project_list)
        self.refresh()

    def refresh(self) -> None:
        self.project_list.clear()
        for p in controller.registry_service.list_projects():
            self.project_list.addItem(p)


def main() -> None:
    app = QApplication([])
    win = MainWindow()
    win.show()
    app.exec()


if __name__ == "__main__":
    main()


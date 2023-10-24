from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                                QLabel, QMessageBox)

class MainWindow(QMainWindow):
    def __init__(self, parent: QWidget | None = None, *args, **kwargs) -> None:
        super().__init__(parent, *args, **kwargs)

        # Basic Layout
        self.central_widget = QWidget()
        self.vLayout = QVBoxLayout()
        self.central_widget.setLayout(self.vLayout)
        self.setCentralWidget(self.central_widget)

        # Window title
        self.setWindowTitle('Calculator')

        self.setStyleSheet("QMainWindow {background-color: #FF5733;}")

    def adjustFixedSize(self):
        # Last implementation
        self.adjustSize()
        self.setFixedSize(self.width(), self.height())

    def addWidgetToVLayout(self, widget: QWidget):
        self.vLayout.addWidget(widget)

    def makeMsgBox(self):
        return QMessageBox(self)
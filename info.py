from PySide6.QtWidgets import QLabel, QWidget
from PySide6.QtCore import Qt
from variables import SMALL_FONT_SIZE

class Info(QLabel):
    def __init__(
    self, text : str, parent: QWidget | None = None # "QWidget | None" means that parent is an optional parameter of the type QWidget, representing the parent widget to which this
    ) -> None:                                         # Info widget will be added, if no parent is specified, it will return None.
        super().__init__(text, parent)
        self.configStyle()

    def configStyle(self):
        self.setStyleSheet(f"font-size: {SMALL_FONT_SIZE}px")
        self.setAlignment(Qt.AlignmentFlag.AlignRight)
        
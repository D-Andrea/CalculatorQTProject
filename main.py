import sys

from main_window import MainWindow
from display import Display
from info import Info, QLabel
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication
from variables import WINDOW_ICON_PATH
from styles import setupTheme
from buttons import Button, ButtonsGrid

if __name__ == "__main__":

    # Creates the application
    app = QApplication(sys.argv)
    setupTheme()
    window = MainWindow()

    # Define Icon
    icon = QIcon(str(WINDOW_ICON_PATH))
    window.setWindowIcon(icon)
    app.setWindowIcon(icon)
  
    # Info
    info = Info('Your Math')
    window.addWidgetToVLayout(info)

    # Display
    display = Display()
    window.addWidgetToVLayout(display)

    # Grid
    buttonsGrid = ButtonsGrid(display, info, window)
    window.vLayout.addLayout(buttonsGrid)

    # Execute everything
    window.adjustFixedSize()
    window.show()
    app.exec()



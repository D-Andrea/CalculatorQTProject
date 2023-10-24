import math
from display import Display
from PySide6.QtCore import Slot
from PySide6.QtWidgets import QPushButton, QGridLayout
from utils import isNumOrDot, isEmpty, isValidNumber
from variables import MEDIUM_FONT_SIZE
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from display import Display
    from main_window import MainWindow
    from info import Info

class Button(QPushButton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs) 
        self.configStyle()

    def configStyle(self):
        font = self.font()
        font.setPixelSize(MEDIUM_FONT_SIZE)
        self.setFont(font)
        self.setMinimumSize(75, 75)

class ButtonsGrid(QGridLayout):
    def __init__(
            self, display: 'Display', info: 'Info', window: 'MainWindow', *args, **kwargs
    ) -> None:
        super().__init__(*args, **kwargs)

        self._gridMask = [
            ['C', '◂', '^', '/'],
            ['7', '8', '9', '*'],
            ['4', '5', '6', '-'],
            ['1', '2', '3', '+'],
            ['',  '0', '.', '='],
        ] 

        self.display = display
        self.info = info
        self.window = window
        self._equation = ''
        self._left = None
        self._right = None
        self._op = None
        self._makeGrid()

    @property
    def equation(self):
        return self._equation
    
    @equation.setter
    def equation(self, value):
        self._equation = value
        self.info.setText(value)

    def _makeGrid(self):
        self.display.eqPressed.connect(self._eq)
        self.display.delPressed.connect(self.display.backspace)
        self.display.clearPressed.connect(self._clear)
        self.display.inputPressed.connect(self._insertToDisplay)
        self.display.operatorPressed.connect(self._operatorClicked)

        # Looping throught rows and data in the gridMask
        for row_number, row_data in enumerate(self._gridMask):
            for column_number, buttonText in enumerate(row_data):
                # Create a Button widget with the given button_text
                button = Button(buttonText)

                # REGEX (see regex "utils.py" file)
                # Checking if the button is neither a number nor a dot and is not empty
                if not isNumOrDot(buttonText) and not isEmpty(buttonText):
                    # If it's a special button, set a CSS class for styling
                    button.setProperty('cssClass', 'specialButton')
                    self._configSpecialButton(button)

                # Add the button to the grid layout at the specified row and column
                self.addWidget(button, row_number, column_number)

                # Create a slot using the _insertButtonTextToDisplay function
                slot = self._makeSlot(self._insertToDisplay, buttonText)
                # Connect the button's click event to the slot
                self._connectButtonClicked(button, slot)

    def _connectButtonClicked(self, button, slot):
        button.clicked.connect(slot)

    def _configSpecialButton(self, button):
        text = button.text()

        if text in '+-/*^':
            self._connectButtonClicked(
                button,
                self._makeSlot(self._operatorClicked, text)
                )
       
        if text == 'C':
            self._connectButtonClicked(button, self._clear)
        
        if text == '=':
            self._connectButtonClicked(button, self._eq)
        
        if text == '◂':
            self._connectButtonClicked(button, self.display.backspace)

    @Slot()
    def _makeSlot(self, func, *args, **kwargs):
        # This function generates and returns a slot function
        # which will call the provided 'func' with any additional args and kwargs
        @Slot(bool)
        def realSlot(_):
            func(*args, **kwargs)
        return realSlot

    @Slot()
    def _insertToDisplay(self, text):
        # This function is called when a button in the grid is clicked
        # and it sets the text of a displau widget to clicked.
        newDisplayValue = self.display.text() + text

        if not isValidNumber(newDisplayValue):
            return

        self.display.insert(text)

    @Slot()
    def _clear(self):
        self._left = None
        self._right = None
        self._op = None
        self.display.clear()
        self.equation = f'Your Math'
    
    # When operator is clicked
    @Slot()
    def _operatorClicked(self, text): # Receives button
        displayText = self.display.text() # 
        self.display.clear() # Clearing the display

        if not isValidNumber(displayText) and self._left is None:
            self._showError("You didn't type anything.")
            return

        # If anything is already at the left place, nothing is done, and the
        # right number is waited.
        if self._left is None:
            self._left = float(displayText)

        self._op = text
        self.equation = f'{self._left} {self._op} ??'

    # Clicking the equal button
    @Slot()
    def _eq(self):
        displayText = self.display.text()

        # Checking if the display is valid
        if not isValidNumber(displayText):
            self._showError('Number not valid')
            return
        elif self._left is None:
            self._showError('Type an operator')
            return
        
        self._right = float(displayText)
        self.equation = f'{self._left} {self._op} {self._right}'
        result = 'error'

        try:
            if '^' in self.equation and isinstance(self._left, float):
                result = math.pow(self._left, self._right)
            else:
                result = eval(self.equation) # Very sensible operation (EVAL)
                # I'm only using it here since it's sure nothing can acess the actual
                # Python terminal
        except ZeroDivisionError:
            self._showError('Zero division error')
        except OverflowError:
            self._showError('Number is too big')

        self.display.clear()
        self.info.setText(f'{self.equation} = {result:.4f}')
        self._left = result
        self._right = None

        if result == 'error': 
            self._left = None

    def _showError(self, text):
        msgBox = self.window.makeMsgBox()
        msgBox.setText(text)
        msgBox.setIcon(msgBox.Icon.Critical)
        msgBox.exec()
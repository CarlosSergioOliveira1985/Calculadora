from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QLineEdit
from PySide6.QtGui import QKeyEvent
from variables import BIG_FONT_SIZE, MINIMUM_WIDTH, TEXT_MARGIN
from utils import isEmpty, isNumOrDot

class Display(QLineEdit):

    eqPressed = Signal()
    delPressed = Signal()
    clearPressed = Signal()
    inputPressed = Signal(str)
    operatorPressed = Signal(str)
    

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.configStyle()

    def configStyle(self):
        margins = [TEXT_MARGIN for _ in range(4)]
        self.setStyleSheet(f'font-size: {BIG_FONT_SIZE}px;')
        self.setMinimumHeight(BIG_FONT_SIZE * 2)
        self.setMinimumWidth(MINIMUM_WIDTH)
        self.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.setTextMargins(*margins)

    def keyPressEvent(self, event: QKeyEvent) -> None:
        text = event.text().strip()
        key = event.key()
        KEYS = Qt.Key

        isEnter = key in [KEYS.Key_Enter, KEYS.Key_Return]
        isDelete = key in [KEYS.Key_Backspace, KEYS.Key_Delete]
        isEsc = key in [KEYS.Key_Escape]
        isOperator = key in[KEYS.Key_Plus, KEYS.Key_Minus, KEYS.Key_Slash, KEYS.Key_Asterisk, KEYS.Key_P]
       

        if isEnter or text == '=':
            self.eqPressed.emit()
            return event.ignore()
        if isDelete or text.lower() == 'd':
            self.delPressed.emit()
            return event.ignore()
        if isEsc or text.lower() == 'c':
            self.clearPressed.emit()
            return event.ignore()
        if isOperator:
            if text.lower()== 'p':
                text = '^'
            self.operatorPressed.emit(text)
            return event.ignore()
        
        if isEmpty(text):
            return event.ignore()
        
        
        if isNumOrDot(text):
            self.inputPressed.emit(text)
            return event.ignore()



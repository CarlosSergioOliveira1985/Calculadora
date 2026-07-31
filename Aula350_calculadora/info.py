from PySide6.QtWidgets import QLabel, QWidget
from variables import MEDIUM_FONT_SIZE, TEXT_MARGIN, MINIMUM_WIDTH
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLineEdit


class Info(QLabel):
    def __init__ (self, text: str, parent: QWidget | None = None) -> None:
        super().__init__(text, parent)
        self.configStyle()

    def configStyle(self):
        self.setStyleSheet(f'font-size: {MEDIUM_FONT_SIZE}px;')
        self.setMinimumHeight(MEDIUM_FONT_SIZE * 2)
        self.setMinimumWidth(MINIMUM_WIDTH)
        self.setAlignment(Qt.AlignmentFlag.AlignRight)
        
        
from PySide6.QtWidgets import QLabel, QScrollArea, QWidget
from PySide6.QtCore import Qt
from variables import SMALL_FONT_SIZE, MINIMUM_WIDTH


class History(QScrollArea):
    """
    Widget de rodapé que mostra o histórico completo de contas já
    finalizadas. Usa um QLabel dentro de um QScrollArea porque um
    QLabel sozinho não tem barra de rolagem, e o histórico pode
    crescer bastante.
    """

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._label = QLabel('')
        self._configLabelStyle()
        self._configScrollArea()

    def _configLabelStyle(self):
        self._label.setStyleSheet(
            f'font-size: {SMALL_FONT_SIZE}px; color: #aaaaaa; padding: 4px;'
        )
        self._label.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignRight)
        self._label.setWordWrap(True)

    def _configScrollArea(self):
        self.setWidget(self._label)
        self.setWidgetResizable(True)
        self.setMinimumWidth(MINIMUM_WIDTH)
        self.setFixedHeight(120)

    def setText(self, text: str):
        self._label.setText(text)

    def text(self) -> str:
        return self._label.text()
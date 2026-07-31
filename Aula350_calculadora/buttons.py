from PySide6.QtWidgets import QPushButton, QGridLayout, QWidget
from variables import MEDIUM_FONT_SIZE
from utils import isNumOrDot, isEmpty, isValidNumber
from display import Display
from PySide6.QtCore import Slot
import math

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from display import Display
    from main_window import MainWindow
    from info import Info
    from history import History


class Button(QPushButton):
    def __init__ (self, *args, **kwargs):
        super().__init__ (*args, **kwargs)
        self.configStyle()
    
    def configStyle(self):
        font = self.font()
        font.setPixelSize(MEDIUM_FONT_SIZE)
        self.setFont(font)
        self.setMaximumSize(500,75)
        self.setCheckable(False)
        

class ButtonsGrid(QGridLayout):
    def __init__(self, display: 'Display', info: 'Info', window: 'MainWindow', history: 'History', *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self._gridMask = [
            ['C', '◀', '^', '/'],
            ['7', '8', '9', '*'],
            ['4', '5', '6', '-'],
            ['1', '2', '3', '+'],
            ['N',  '0', '.', '='],
        ]
        self.display = display
        self.info = info
        self.window = window
        self.history = history  # NOVO: widget de histórico no rodapé
        self._equation = ''
        self._equationInitialValue = "Sua Conta"
        self._left = None
        self._right = None
        self._op = None

        self._history = []  # NOVO: lista com todas as contas já finalizadas

        self.equation = self._equationInitialValue
        self._makeGrid()

    @property
    def equation(self):
        return self._equation

    
    @equation.setter
    def equation(self, value):
        self._equation = value
        self.info.setText(value)

    def vouApagarVocê(self, *args):
        print('Signal recebido por "vouapagarVocê" em', type(self).__name__ , args)

    def _makeGrid(self):
        self.display.eqPressed.connect(self._eq)
        self.display.delPressed.connect(self._backspace)
        self.display.clearPressed.connect(self._clear)
        self.display.inputPressed.connect(self._insertToDisplay)
        self.display.operatorPressed.connect(self._configLeftOp)
        
        for i, row in enumerate(self._gridMask):
            for j,buttonText in enumerate(row):
                button = Button(buttonText)

                if not isNumOrDot(buttonText) and not isEmpty(buttonText):
                    button.setProperty('cssClass', 'specialButton')
                    self._configSpecialButton(button)
                self.addWidget(button, i, j)
                slot = self._makeSolt(self._insertToDisplay,buttonText)
                self._connectButtonClicked(button, slot)
                

    def _connectButtonClicked(self, button, slot):
        button.clicked.connect(slot)

    def _configSpecialButton(self, button):
        text = button.text()

        if text == 'C':
            # slot = self._makeSolt(self.display.clear)
            self._connectButtonClicked(button, self._clear)
            #button.clicked.connect(self.display.clear)
            
        if text == '◀':            
            self._connectButtonClicked(button, self.display.backspace)

        if text == 'N':            
            self._connectButtonClicked(button,self._invertNumber)

        if text in '+-*/^':            
            self._connectButtonClicked(
                button,
                self._makeSolt(self._configLeftOp, text))
            
        if text in '=':            
            self._connectButtonClicked(button, self._eq)
        
            
            
        
    @Slot()
    def _makeSolt(self,func, *args, **kwargs):
        @Slot(bool)
        def realsSlot(_):
            func(*args, **kwargs)
        return realsSlot
    
    @Slot()

    def _invertNumber(self):
        displayText = self.display.text()
        if not isValidNumber (displayText):
            return 
        newNumber = -float(displayText)
        self.display.setText(str(newNumber))


    @Slot()
    def _insertToDisplay(self, text):
        
        newDisplayValue = self.display.text() + text

        if not isValidNumber (newDisplayValue):
            return
        self.display.insert(text)
        self.display.setFocus()
        
    @Slot()
    def _clear(self):
        self._left = None
        self._right = None
        self._op = None

        self.equation = self._equationInitialValue
        self.display.clear()
        self.display.setFocus()
    @Slot()
    def _configLeftOp(self, text):
        displayText = self.display.text()  # Deverá ser meu número _left
        self.display.clear()  # Limpa o display
        self.display.setFocus()

        # Se a pessoa clicou no operador sem
        # configurar qualquer número
        if not isValidNumber(displayText) and self._left is None:
            self._showError('Você não digitou nada.')
            return

        # Se houver algo no número da esquerda,
        # não fazemos nada. Aguardaremos o número da direita.
        if self._left is None:
            self._left = float(displayText)

        self._op = text
        self.equation = f'{self._left} {self._op} ??'

    @Slot()
    def _eq(self):
        displayText = self.display.text()

        if not isValidNumber(displayText) or self._left is None:
            print('Sem nada para a direita')
            self._showError('Conta incompleta.')
            return

        self._right = float(displayText)
        self.equation = f'{self._left} {self._op} {self._right}'
        result = 'error'
        
        try:   
            if  '^'  in self.equation and isinstance(self._left, float):
                result = math.pow(self._left, self._right)
                #result = eval(self.equation.replace('^', '**'))
            
            else:
                result = eval(self.equation)
                   
        except ZeroDivisionError:
            self._showError('Você está tentando dividir por 0')
        except OverflowError:
            self._showError('Sua conta tem um resultado muito grande')

        self.display.clear()
        self.info.setText(f'{self.equation} = {result}')

        # NOVO: guarda a conta finalizada no histórico e atualiza
        # o widget de rodapé (se ele tiver sido passado)
        linha = f'{self.equation} = {result}'
        self._history.append(linha)
        if self.history is not None:
            self.history.setText('\n'.join(self._history))

        self._left = result
        self._right = None
        self.display.setFocus()

        if result =='error':
            self._left = None

    @Slot()
    def _backspace(self):
        self.display.backspace()
        self.display.setFocus()

    def _makeDialog(self, text):
        msgBox = self.window.makeMsgBox()
        msgBox.setText(text)
        return msgBox

    def _showError(self, text):
        msgBox = self._makeDialog(text)
        msgBox.setIcon(msgBox.Icon.Critical)
        msgBox.exec()
        self.display.setFocus()

    def _showInfo(self, text):
        msgBox = self._makeDialog(text)
        msgBox.setIcon(msgBox.Icon.Information)
        msgBox.exec()
        self.display.setFocus()
        
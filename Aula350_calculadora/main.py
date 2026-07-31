import sys


from display import Display
from info import Info
from history import History
from main_window import MainWindow
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication
from variables import WINDOW_ICON_PATH_ICO
from style import setupTheme
from buttons import Button, ButtonsGrid

if __name__ == '__main__':
    # Cria a aplicação

    
    app = QApplication(sys.argv)
    setupTheme(app)

    window = MainWindow()

    # Define o ícone
    icon = QIcon(str(WINDOW_ICON_PATH_ICO))
    
    window.setWindowIcon(icon)
    app.setWindowIcon(icon)

    # Info

    info = Info('Sua Conta')
    window.addWidgetToVLayout(info)


    # Display
    display = Display()
    window.addWidgetToVLayout(display)

    # Histórico (rodapé)
    history = History()

    #Grid

    buttonsGrid = ButtonsGrid(display, info, window, history)
    window.vLayout.addLayout(buttonsGrid)

    # Histórico é adicionado por último, para ficar no rodapé
    # (embaixo dos botões)
    window.addWidgetToVLayout(history)

       
   
    # Executa tudo
    window.adjustFixedSize()
    window.show()

    sys.exit(app.exec())
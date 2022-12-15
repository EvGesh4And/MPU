from PyQt5.QtGui import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from Development import *

"""
Файл BlockDiagram.py является частью модуля Proc.
Основное окно, в котором пользователь может собрать блок-схему.
Содержит меню, в котором представлены функции программы
"""


class MainWindow(QMainWindow):
    def __init__(self):
        """
        Метод определяет Главное окно
        """

        # Инициализация родительского класса
        super().__init__()

        # Название главного окна
        self.setWindowTitle("ПК 'Экстремум'. Модуль процедурного управления")

        # Добавление логотипа главному окну
        self.setWindowIcon(QIcon("logo_Extremum.png"))

        # Задание размера окна, который равен размеру всего экрана
        self.setGeometry(QDesktopWidget().screenGeometry(-1))

        # Флаг, который задает окно поверх всех окон
        self.setWindowFlag(Qt.WindowStaysOnTopHint)

        # Задание логотипа Комиты
        self.comita = QLabel(self)
        self.comita.setScaledContents(True)
        self.comita.setPixmap(QPixmap("comita.png"))
        self.comita.show()


        self.tab_main = QTabWidget(self)
        self.tab_main.move(0, 0)

        self.tab_controller = Development(self)
        self.tab_controller1 = Development(self)
        self.tab_main.addTab(self.tab_controller, "Разработка")
        self.tab_main.addTab(self.tab_controller1, "Исполнение")

    def resizeEvent(self, e):
        self.comita.setGeometry(self.width() - 180, self.height() - 80, 160, 50)
        self.tab_main.resize(self.geometry().width(), self.geometry().height())

qss = """ 
QTabWidget::tab-bar {
    alignment: center;
}

QTabWidget::pane { /* The tab widget frame */
    border-top: 2px solid #C2C7CB;
}

QTabBar::tab {
    border: 2px solid #C4C4C3;
    min-width: 24ex;
    min-height: 5ex;
    padding: 5px;
}

QTabBar::tab:selected  {
    border-color: #1dacd6;
    font: 14pt;
}  

QTabBar::tab:!selected {
    border-color:rgb(220, 220, 220);
    font: 14pt;
}


QMenuBar {
    spacing: 5px; /* spacing between menu bar items */
    font: 12pt;
}

QMenuBar::item {
    padding: 2px 4px;
    background: transparent;
    border-radius: 4px;
}

QMenuBar::item:selected { /* when selected using mouse or keyboard */
    border: 1px solid #05B8CC;
}

"""

if __name__ == "__main__":
    app = QApplication([''])
    app.setStyleSheet(qss)
    window = MainWindow()
    window.show()
    app.exec_()

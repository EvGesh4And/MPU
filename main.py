from PyQt5.QtGui import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from help import *
from BlockDiagram import *

"""
Файл BlockDiagram.py является частью модуля Proc.
Основное окно, в котором пользователь может собрать блок-схему.
Содержит меню, в котором представлены функции программы
"""


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        """
        Метод определяет Главное окно
        """

        # Инициализация родительского класса
        super().__init__()

        # Название главного окна
        self.setWindowTitle("ПК 'Экстремум'. Модуль процедурного управления")

        # Добавление логотипа главному окну
        self.setWindowIcon(QtGui.QIcon("logo_Extremum.png"))

        # Задание размера окна, который равен размеру всего экрана
        self.setGeometry(QDesktopWidget().screenGeometry(-1))

        # Флаг, который задает окно поверх всех окон
        self.setWindowFlag(QtCore.Qt.WindowStaysOnTopHint)

        # Переменные блоков

        # Списки блоков

        # Задание логотипа Комиты
        self.comita = QLabel(self)
        self.comita.setScaledContents(True)
        self.comita.setPixmap(QtGui.QPixmap("comita.png"))
        self.comita.show()

        # Создание вложенных списков
        self.enterButton = self.pressedButton = None
        self.menubar = QMenuBar(self)
        self.setMenuBar(self.menubar)
        self.menubar.setObjectName("menubar")
        self.razrabotka = self.menubar.addAction("Разработка")
        self.inspolnenie = self.menubar.addAction("Исполнение")

        self.razrab_wid = Razrabotka()
        # Вызов команд при нажатии на кнопки
        self.razrabotka.triggered.connect(self.open_razrab_wid)

    def open_razrab_wid(self):
        print("Hi")
        # Задание размера окна, который равен размеру всего экрана
        print(self.getClientRects())
        self.razrab_wid.setGeometry(self.getClientRects())
        self.razrab_wid.show()


    def resizeEvent(self, e):
        self.comita.setGeometry(self.width() - 180, self.height() - 70, 160, 50)


    def add_begin(self):
        """
        Метод создания элемента класса Начало
        :return: виджет на главном окне
        """
        self.begin = Begin(self)
        self.begin.show()
        self.list_begin.append(self.begin)
        print("Add begin")
        self.begin.setGeometry(140, 73, 365, 243)
        self.begin.set_name(f"{len(self.list_begin)}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec_()

import os
import sys

from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5 import QtGui
import csv
from contextmenu import *
from PyQt5 import *
from properties import *
from PyQt5.QtWidgets import *
from indicator import *

"""
Файл begin.py является частью модуля Proc.
Описание элемента блок-схемы Начало
Отображает название элемента, которое пользователь вводит на вкладке Основное Окна свойств блока
"""
class Begin(QtWidgets.QWidget):
    def __init__(self, parent=None, text="", node_child=""):
        """
        Метод определяет блок "Начало", его атрибуты: text - текстовое поле, node_child - для связи с нижеследующим блоком
        """
        super().__init__(parent)
        self.active = False
        self.parent      = parent
        self.text        = text
        self.node_child  = node_child
        self.font        = QFont('Times', 14)
        self.font2       = QFont('Times', 9)
        self.label       = QLabel(self.text, self)

        self.pic         = QLabel("Begin", self)
        self.mouse_x     = 0
        self.mouse_y     = 0

        menu             = ContextMenu()
        self.is_moveable = True
        self.moveable    = True
        self.proper      = Properties()
        self.filename    = ""
        self.contextMenu = QtWidgets.QMenu(self)
        self.fix_pos     = self.contextMenu.addAction("Зафиксировать положение")
        self.delete      = self.contextMenu.addAction("Удалить")
        sizeObject       = QDesktopWidget().screenGeometry(-1)
        self.main_width  = sizeObject.width()
        self.main_height = sizeObject.height()
        self.label2      = QLabel("Начало", self)
        self.table       = QTableWidget(self)
        self.name        = QLineEdit(self)


        self.resize(205, 120)
        self.setWindowTitle("Begin")

        self.proper.set_element(self)
       # self.delet.set_element(self)
        self.table.setColumnCount(1)
        self.pic.setScaledContents(True)
     #   self.table.setGeometry(35, 60, 300, 150)
        vh = self.table.verticalHeader()
        vh.setDefaultSectionSize(15)
        hh = self.table.horizontalHeader()
        hh.setDefaultSectionSize(300)
        self.table.setHorizontalHeaderLabels([' '])
        self.setFont(self.font)
        self.pic.setPixmap(QtGui.QPixmap("Begin.png"))
       # self.pic.setGeometry(0, 0, self.width(), self.height())
        self.label2.setGeometry(70, 23, 100, 20)
        print(f"{self.main_width} | {self.main_height}")
        self.setAcceptDrops(True)
       # self.text.setGeometry(30, 55, 290, 100)
       # self.text.setReadOnly(True)
        menu.show()
        #  self.settings = QtCore.QSettings()
        self.fix_pos.triggered.connect(self.fix_position)
        self.delete.triggered.connect(self.deleted)
        self.add_indicator()
        self.setGeometry(1500, 1000, 374, 240)
     #   self.name.setGeometry(35, 60, 300, 25)
        self.name.setReadOnly(True)
        self.real_name = "_begin"

    def scan_state_node_parents(self):
        if self.node_parents:
            active_parents = True
            for node in self.node_parents:
                if not node.active:
                    active_parents = False
            if active_parents:
                self.set_active_state(True)
                for node in self.node_parents:
                    node.set_active_state(False)    
        else:
            self.set_active_state(False)

    def set_active_state(self, bool_state):
        self.active = bool_state

    def get_name(self) -> str:
        return self.real_name
    
    def set_name(self, name):
        self.name.setText(name)
        self.real_name = name.replace("_begin", "") + "_begin"
        print(f" MY NAME IS {self.real_name}")

    def save_project(self, path):
        name = self.get_name()
        # print(name)

        file_exist = os.path.exists(f"{path}/{name}/{name}")
        if(not file_exist):
            os.mkdir(f"{path}/{name}")
        
        with open(f"{path}/{name}/{name}", "w") as config:
            # config = csv.reader(config_file, delimiter=",")
            config.write("type,name")
            config.write(f"x,{self.x()}")
            config.write(f"y,{self.y()}")
            config.write(f"indicator1,{self.indicator.get_name()}")

    def add_indicator(self):
        """
        Метод, описывающий индикатор соединения элемента с другими
        :return:
        """
        self.indicator = Indicator(self)
        self.indicator.show()
        self.indicator.setGeometry(172, 201, 27, 38)

    def set_var_filename(self, filename):
        """
        Метод для получения имени файла, который пользователь выбрал для получения переменных
        :param filename:
        :return:
        """
        self.filename = filename
        print("Opretation")
        self.proper.set_var_filename(filename)

    def ev(self, ev):
        """

        :param ev:
        :return:
        """
        if ev.type() == QtCore.QEvent.KeyPress and ev.key() in (
                QtCore.Qt.Key_Enter,
                QtCore.Qt.Key_Return,
                ):
            self.focusNextPrevChild(True)
        return super().event(ev)

    def resizeEvent(self, a0):
        """
        Метод адаптации размеров элемента
        :param a0:
        :return:
        """
        self.pic.setGeometry(10, 10, self.width() - 20, self.height() - 20)
        print(f" w = {self.width()} | h = {self.height()}")
       # self.table.setGeometry(self.width() - 335, self.height() - 180, 300, 150)
        self.indicator.setGeometry(int(((self.width()) - 10) / 2), self.height() - 40, 27, 38)
        self.name.setGeometry(35, int(self.height()*0.17)+15, self.width() - 77, 25)
        self.label2.setGeometry(int(self.width()*0.2), int(self.height()*0.06), 100, 28)
        self.table.setGeometry(35, int(self.height()*0.17)+15, self.width() - 76, self.height() - 80)
        self.table.setMaximumHeight(int(self.height())-int(self.height()*0.3))

    def set_child(self, node_child):
        """
        Метод добавления связи с нижеследующим элементом
        :param node_child:
        :return:
        """
        self.node_child = node_child

    def mouseDoubleClickEvent(self, event):
        """
        При двойном нажатии мышью на элемент вызывается Окно свойств
        :param event:
        :return:
        """
        self.proper.show()

    def mousePressEvent(self, event):
        """
        Метод, вызываемый при нажатии мыши
        :param event:
        :return:
        """
        self.mouse_x = self.x()
        self.mouse_y = self.y()
        self.xx = event.globalX()
        self.yy = event.globalY()

    def mouseMoveEvent(self, event):
        """
        Метод перемещения элемента по рабочей области
        :param event:
        :return:
        """
        if (self.is_moveable):
            if (self.parent != None):
                x = event.globalX()
                y = event.globalY()
                move_x = x - (self.xx - self.mouse_x)
                move_y = y - (self.yy - self.mouse_y)
                if move_x > self.parent.width() - self.width():
                    move_x = self.parent.width() - self.width()
                if move_x < 0:
                    move_x = 0
                    # self.mouse_x = 10
                if move_y < 0:
                    move_y = 0
                if move_y > self.parent.height() - self.height():
                    move_y = self.parent.height() - self.height()

                self.move(move_x, move_y)
            else:
                x = event.globalX()
                y = event.globalY()
                move_x = x - (self.xx - self.mouse_x)
                move_y = y - (self.yy - self.mouse_y)
                if move_x > self.main_width - self.width():
                    move_x = self.main_width - self.width()
                if move_x < 0:
                    move_x = 0
                    # self.mouse_x = 10
                if move_y < 0:
                    move_y = 0
                if move_y > self.main_height - self.height():
                    move_y = self.main_height - self.height()
                self.move(move_x, move_y)

    def setMoveable(self, ind):
        self.moveable = ind


    def save_logs(self):
        """
        Метод сохранения настроек элемента
        :return:
        """
        self.settings.setValue("Geometry_X" , self.x())
        self.settings.setValue("Geometry_Y" , self.y())
        self.settings.setValue("Moveable" , str(self.is_moveable))
        print(str(self.x()) + " | " + str(self.y()))

    def contextMenuEvent(self, event):
        """
        По нажатию правой кнопки по элементу появляется контекстное меню
        :param event:
        :return:
        """
        print("Открылось контекстное меню")
        # self.contextMenu.move(self.x(), self.y())
        # self.contextMenu.show()
        action = self.contextMenu.exec_(self.mapToGlobal(event.pos()))

    def add_parent(self):
        """
        Метод добавления связи с предыдущим элементом
        :return:
        """
        print("Нажали на кнопку Удали")

    def add_child(self):
        """
        Метод добавления связи с нижеследующим элементом
        :return:
        """
        print("Нажали на кнопку Удали")

    def fix_position(self):
        """
        Метод фиксации положения элемента
        :return:
        """
        print("Нажали на кнопку Удали")
        self.is_moveable = not self.is_moveable

    def deleted(self):
        """
        Метод удаления объекта с главного окна
        :return:
        """
        self.reply = QMessageBox.question(
            self, "Удаление",
            "Вы действительно хотите удалить блок Начало?",
            QMessageBox.Yes | QMessageBox.No )

        if self.reply == QMessageBox.Yes:
            self.close()
        else:
            pass

if __name__ == "__main__":
    # QtCore.QCoreApplication.addLibraryPath("./")
    app = QtWidgets.QApplication(sys.argv)
    window = Begin()
    window.show()
    app.exec_()

#comm
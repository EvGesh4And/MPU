from PyQt5.QtGui import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

"""
Файл BlockDiagram.py является частью модуля Proc.
Основное окно, в котором пользователь может собрать блок-схему.
Содержит меню, в котором представлены функции программы
"""


class Razrabotka(QtWidgets.QMainWindow):
    def __init__(self):
        """
        Метод определяет Главное окно
        """
        super().__init__()

        # Задаем флаг, который задает его поверх всех окон
        self.setWindowFlag(QtCore.Qt.WindowStaysOnTopHint)

        # Переменные блоков
        self.begin = None
        self.inputdata = None
        self.operation = None
        self.cond = None
        self.cycle = None
        self.end = None
        self.marker_action = True
        self.title = None
        self.table = None
        self.edit = None
        self.font = QFont('Times', 14)

        # Списки блоков
        self.list_begin = []
        self.list_inputdata = []
        self.list_cond = []
        self.list_operations = []
        self.list_cycle = []
        self.list_end = []
        self.list_title = []

        # Задание логотипа Комиты
        self.comita = QLabel(self)
        self.comita.setScaledContents(True)
        self.comita.setPixmap(QtGui.QPixmap("comita.png"))
        self.setFont(self.font)
        self.comita.show()

        # Создание вложенных списков
        self.enterButton = self.pressedButton = None
        self.menubar = QMenuBar(self)
        self.setMenuBar(self.menubar)
        self.menubar.setObjectName("menubar")

        self.menu = self.menubar.addMenu("Меню")

        self.create = self.menu.addAction("Создать новый файл")
        self.save = self.menu.addAction("Сохранить файл")
        self.open = self.menu.addAction("Открыть файл")
        self.connect = self.menubar.addMenu("Связь")
        self.opc_ua = self.connect.addAction("OPC UA")
        self.get_names = self.connect.addAction("Получить имена тэгов")

        # Вызов команд при нажатии на кнопки
        self.create.triggered.connect(self.CreateFile)
        self.save.triggered.connect(self.SaveFile)
        self.open.triggered.connect(self.OpenFile)
        self.opc_ua.triggered.connect(self.Opc)
        self.get_names.triggered.connect(self.GetData)

        # Создание вложенных списков
        self.add_elem = self.menubar.addMenu("Добавить элемент")
        self.begin1 = self.add_elem.addAction("Начало")
        self.inputdata1 = self.add_elem.addAction("Ввод/вывод данных")
        self.condition1 = self.add_elem.addAction("Условие")
        self.operation = self.add_elem.addAction("Операция")
        self.cycle = self.add_elem.addAction("Цикл")
        self.end = self.add_elem.addAction("Конец")
        self.inscription = self.add_elem.addAction("Комментарий")
        self.get_help = self.menubar.addAction("Справка")

        # Вызов команд при нажатии на кнопки
        self.begin1.triggered.connect(self.add_begin)
        self.inputdata1.triggered.connect(self.add_inputdata)
        self.condition1.triggered.connect(self.add_cond)
        self.operation.triggered.connect(self.add_operation)
        self.cycle.triggered.connect(self.add_cycle)
        self.end.triggered.connect(self.add_end)
        self.inscription.triggered.connect(self.AddTitle)
        self.get_help.triggered.connect(self.GetHelp)

        self.setObjectName("MainWindow")
        self.setStyleSheet("#MainWindow{border-image:url(grey.png)}")
        self.palette = QPalette()
        self.palette.setBrush(QPalette.Background, QBrush(QPixmap("grey.png")))
        self.setPalette(self.palette)
        self.help = Help()

        self.indicator_begin = ""
        self.indicator_end = ""
        self.indicator_pairs = {}
        self.indicator_begins = []
        self.indicator_ends = []

        self.timer = QTimer()
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.slot_timer_timeout)

        self.saveproject_widget = MPU_save_project_widget()
        self.saveproject_widget.set_core(self)
        # self.timer.start()

    def slot_save_triggered(self):
        print("save")

    def slot_timer_timeout(self):
        self.update()

    def resizeEvent(self, e):
        self.comita.setGeometry(self.width() - 180, self.height() - 70, 160, 50)

    def Opc(self):
        print("OPC")

    def indicator_press(self, indicator):
        if (self.indicator_begins.__contains__(indicator)):
            self.indicator_in_arrows(indicator)
        else:
            if (self.indicator_ends.__contains__(indicator)):
                self.indicator_in_arrows(indicator)
            else:
                self.indicator_not_in_arrows(indicator)

    def indicator_in_arrows(self, indicator):
        if (self.indicator_begins.__contains__(indicator)):
            if (self.indicator_pairs[indicator] == ""):
                self.indicator_begins.remove(indicator)
                self.indicator_pairs.pop(indicator)
                self.indicator_begin = ""
                indicator.set_picture_off()
                indicator.set_inactive()
            else:
                indicator.set_picture_off()
                indicator.set_inactive()
                self.indicator_pairs[indicator].set_picture_off()
                self.indicator_pairs[indicator].set_inactive()
                self.indicator_begins.remove(indicator)
                self.indicator_ends.remove(self.indicator_pairs[indicator])
                self.indicator_pairs.pop(indicator)
                self.indicator_begin = ""
            if (self.indicator_ends.__contains__(indicator)):
                indicator.active = True

    def set_begin(self, indicator):
        if (indicator.active == True):
            self.indicator_begin = indicator
            self.indicator_begin.set_picture_on()
            self.indicator_pairs[indicator] = ""
            self.indicator_begins.append(indicator)

    def unset_begin(self, indicator):
        if (indicator == False):
            self.indicator_begin = ""
            # indicator set picture
            indicator.set_picture_off()
            self.indicator_begins.remove(indicator)

    def set_end(self, indicator):
        if (indicator.active == True):
            self.indicator_ends.append(indicator)
            # indicator set picture
            indicator.set_picture_on()
            self.indicator_pairs[self.indicator_begin] = indicator
            self.indicator_begin = ""
            # self.indicator_ends.append

    def indicator_not_in_arrows(self, indicator):
        if (self.indicator_begin == ""):
            self.set_begin(indicator)
        else:
            if (self.indicator_begin == indicator):
                self.unset_begin(indicator)
            else:
                self.set_end(indicator)

    def paintEvent(self, event: PyQt5.QtGui.QPaintEvent):

        self.painter = QPainter(self)
        pen = QPen()
        pen.setWidth(10)
        pen.setColor(QColor(0, 0, 255))
        # self.painter.begin(self)
        self.painter.setPen(pen)
        if (len(self.indicator_ends) != 0):
            for begin in self.indicator_begins:
                if (self.indicator_pairs[begin] != ""):
                    # x1 = begin.parent.x() + begin.x() + 14
                    # y1 = begin.parent.y() + begin.y() + begin.height()

                    # x2 = self.indicator_pairs[begin].parent.x() + self.indicator_pairs[begin].x()
                    # y2 = self.indicator_pairs[begin].parent.y() + self.indicator_pairs[begin].y()
                    # self.painter.drawLine(x1,y1,x2,y2)
                    self.draw_arrow(event, begin, self.indicator_pairs[begin])
                print(f"{self.indicator_pairs[begin]}")
        self.painter.end()

    def draw_arrow(self, event, ind1, ind2):
        x1 = ind1.parent.x() + ind1.x() + int(ind1.height() / 2) - 5
        y1 = ind1.parent.y() + ind1.y() + int(ind1.height() / 2) + 5

        x2 = ind2.parent.x() + ind2.x() + int(ind2.height() / 2) - 5
        y2 = ind2.parent.y() + ind2.y() + int(ind2.height() / 2) + 5
        self.painter.drawLine(x1, y1, x2, y2)

    def GetData(self):
        """
        Метод получения названий переменных из файла, который выбрал пользователь
        :return: переменные, которые содержатся в этом файле
        filename - путь к файлу, который выбрал пользователь
        """
        self.filename, _ = QFileDialog.getOpenFileName()
        print(f"Нажали на Выгрузить данные из файла: {self.filename}")
        with open(self.filename) as r_file:
            file_reader = csv.reader(r_file, delimiter=";")
            count = 0
            for row in file_reader:
                if count == 0:
                    print(row[0])
                else:
                    print(f'{row}')
                count += 1
            print(f'Всего в файле {count} строк с данными.')
        self.set_var_filename()

    def GetHelp(self):
        self.help.show()

    def CreateFile(self):
        """
        Метод создания нового файла
        :return:
        """
        # self.update()
        print("Нажали на Cоздать файл")

    def load_project(self, project_name):
        print(f"{project_name}")

    def save_project(self, project_name):
        print(f"{project_name}")
        file_exist = os.path.exists(f".config_MPU/{project_name}")
        if (not file_exist):
            os.mkdir(f".config_MPU/{project_name}")

        with open(f".config_MPU/{project_name}/{project_name}", "w") as config:
            config.write("type:name\n")
            for begin in self.list_begin:
                config.write(f"begin:{begin.get_name()}\n")
                begin.save_project(f".config_MPU/{project_name}")
            for inputdata in self.list_inputdata:
                config.write(f"inputdata:{inputdata.get_name()}\n")
                inputdata.save_project(f".config_MPU/{project_name}")
            for cond in self.list_cond:
                config.write(f"cond:{cond.get_name()}\n")
                cond.save_project(f".config_MPU/{project_name}")
            for operation in self.list_operations:
                config.write(f"operation:{operation.get_name()}\n")
                operation.save_project(f".config_MPU/{project_name}")

            for cycle in self.list_cycle:
                config.write(f"cycle:{cycle.get_name()}\n")
                cycle.save_project(f".config_MPU/{project_name}")
            for end in self.list_end:
                config.write(f"end:{end.get_name()}\n")
                end.save_project(f".config_MPU/{project_name}")

            # for title in self.list_title:
            #     config.write(f"title:{title.get_name()}\n")

    def SaveFile(self):
        """
        Метод сохранения файла с созданной пользователем блок-схемой
        :return:
        """
        # Название главного окна
        self.saveproject_widget.setWindowTitle("Сохранение файла")
        # Добавление логотипа к окну
        self.saveproject_widget.setWindowIcon(QtGui.QIcon("logo.png"))

        self.saveproject_widget.setWindowFlag(QtCore.Qt.WindowStaysOnTopHint)
        self.saveproject_widget.show()

        self.update()
        print("Нажали на Сохранить файл")

    def OpenFile(self):
        """
        Метод открытия уже существующего файла с блок-схемой
        :return:
        """
        print("Нажали на Открыть файл")

    def set_var_filename(self):
        """
        Метод для передачи имени файла, который пользователь выбрал для получения переменных
        Перебираются все элементы списка и для них задается файл с тэгами
        :return:
        """
        print(len(self.list_operations))
        for oper in self.list_operations:
            oper.set_var_filename(self.filename)

        for beg in self.list_begin:
            beg.set_var_filename(self.filename)

        for cond in self.list_cond:
            cond.set_var_filename(self.filename)

        for inp in self.list_inputdata:
            inp.set_var_filename(self.filename)

        for cyc in self.list_cycle:
            cyc.set_var_filename(self.filename)

        for end in self.list_end:
            end.set_var_filename(self.filename)

    def Editor(self):
        """
        Метод отображения Редактора выражений
        edit - объект класса Editor
        :return: виджет редактора выражений
        """
        print("Нажали на Редактор")
        self.edit = Editor()
        self.edit.show()

    def InitTitle(self):
        """
        Метод инициализации добавления комментария
        title - объект класса Title
        :return: виджет на главном окне
        """
        title = Title(self)
        title.show()
        # title.setGeometry(500, 40, 3650, 2500)

    # self.title.setWidgetResizable(True)

    def AddTitle(self):
        """
        Метод добавления комментария
        :return:
        """
        self.InitTitle()
        self.list_title.append(self.title)
        # self.title.set_name(f"{len(self.list_title)}")
        print("Нажали на кнопку Добавить надпись")

    def RemoveBlock(self):
        """
        НЕ ИСПОЛЬЗУЕТСЯ
        Метод удаления блока
        :return:
        """
        self.remove_begin()
        print("нажали и Удалили блок")

    # def setup_init_table(self):
    #     """
    #     НЕ ИСПОЛЬЗУЕТСЯ
    #     Метод добавления всех элементов в таблицу
    #     :return:
    #     """
    #     self.table = Table(self)
    #     self.table.show()
    #     self.add_begin()
    #     self.add_inputdata()
    #     self.add_cond()
    #     self.add_cycle()
    #     self.add_operation()
    #     self.add_end()
    #     #self.add_buttons()
    #     # self.add_context_menu()
    #     # self.contextMenuEvent()
    #     print("setup")

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
        menu = ContextMenu()
        menu.show()

    def add_inputdata(self):
        """
        Метод создания элемента класса Ввод/Вывод
        :return: виджет на главном окне
        """
        self.inputdata = InputData(self)
        self.inputdata.show()
        self.list_inputdata.append(self.inputdata)
        print("Add begin")
        self.inputdata.setGeometry(140, 73, 365, 243)
        self.inputdata.set_name(f"{len(self.list_inputdata)}")

    def add_cond(self):
        """
        Метод создания элемента класса Условие
        :return: виджет на главном окне
        """
        self.cond = Cond(self)
        self.cond.show()
        self.list_cond.append(self.cond)
        self.cond.setGeometry(140, 73, 375, 238)
        self.cond.set_name(f"{len(self.list_cond)}")

    def add_operation(self):
        """
        Метод создания элемента класса Операция
        :return: виджет на главном окне
        """
        self.operation = Operation(self)
        self.operation.show()
        self.list_operations.append(self.operation)
        self.operation.setGeometry(140, 73, 365, 243)
        self.operation.set_name(f"{len(self.list_operations)}")

    def add_cycle(self):
        """
        Метод создания элемента класса Цикл
        :return: виджет на главном окне
        """
        self.cycle = Cycle(self)
        self.cycle.show()
        self.list_cycle.append(self.cycle)
        self.cycle.setGeometry(140, 73, 374, 238)
        self.cycle.set_name(f"{len(self.list_cycle)}")

    def add_end(self):
        """
        Метод создания элемента класса Конец
        :return: виджет на главном окне
        """
        self.end = End(self)
        self.end.show()
        self.list_end.append(self.end)
        self.end.setGeometry(140, 73, 365, 234)
        self.end.set_name(f"{len(self.list_end)}")

    def add_context_menu(self):
        """
        Метод создания контекстного меню
        :return:
        """
        menu = ContextMenu(self)
        menu.show()
        menu.setGeometry(700, 300, 300, 300)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec_()


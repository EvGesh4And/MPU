import sys
from PyQt5 import QtWidgets
from PyQt5 import *


class ContextMenu(QtWidgets.QTreeWidget):
    def __init__(self, parent = None):
        QtWidgets.QTreeWidget.__init__(self, parent)

    def contextMenuEvent(self, event):
        contextMenu = QtWidgets.QMenu(self)
        add_parent = contextMenu.addAction("добавить родителя")
        self.create.triggered.connect(self.CreateFile)
        add_child = contextMenu.addAction("добавить ребенка")
        fix_pos = contextMenu.addAction("Зафиксировать положение")
        quit = contextMenu.addAction("Выйти")

        action = contextMenu.exec_(self.mapToGlobal(event.pos()))


if __name__ == "__main__":
    # QtCore.QCoreApplication.addLibraryPath("./")
    app = QtWidgets.QApplication(sys.argv)
    window = ContextMenu()
    window.show()
    app.exec_()

#comm
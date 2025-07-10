"""
DROITEREG - Main 
"""

import os
import sys
import ressource
from PyQt6 import QtCore
from PyQt6.QtGui import QIcon
import fonctions_droitereg as df
from ui_droitereg import Ui_MainWindow
from PyQt6.QtWidgets import QApplication, QMainWindow

def ressource_path(relative_path):
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui_main_window = Ui_MainWindow()
        self.ui_main_window.setupUi(self)
        self.setWindowTitle("DROTIEREG")
        self.setWindowIcon(QIcon(ressource_path('icon_droitereg.ico')))

        df.fillAdjustTableWidget(self.ui_main_window.tableWidget_data)

        self.ui_main_window.pushButton_remplissage.clicked.connect(lambda: df.remplissage(self))
        self.ui_main_window.pushButton_droitereg.clicked.connect(lambda: df.droitereg(self))
        self.ui_main_window.pushButton_zero.clicked.connect(lambda: df.zero(self))
        self.ui_main_window.pushButton_print.clicked.connect(lambda: df.print(self))

        self.ui_main_window.tableWidget_data.installEventFilter(self)

    def eventFilter(self, source, event):
        if (source == self.ui_main_window.tableWidget_data and
            event.type() == QtCore.QEvent.Type.KeyPress and 
            event.key() in (QtCore.Qt.Key.Key_Return, QtCore.Qt.Key.Key_Enter)):
            
            current = self.ui_main_window.tableWidget_data.currentIndex()
            nextIndex = current.sibling(current.row() + 1, current.column())
            if nextIndex.isValid():
                self.ui_main_window.tableWidget_data.setCurrentIndex(nextIndex)
                self.ui_main_window.tableWidget_data.edit(nextIndex)
                return True  # événement traité

        return super().eventFilter(source, event)

def main():
    app = QApplication([])
    window = Window()
    window.show()
    app.exec()

if __name__ == "__main__":
    main()
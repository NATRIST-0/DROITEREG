"""
DROITEREG - Main 

"""

import os
import sys
import ressource
from PyQt6 import QtGui
from PyQt6 import QtCore
from PyQt6.QtGui import QIcon
import fonctions_droitereg as df
from ui_droitereg import Ui_MainWindow
from PyQt6.QtWidgets import QApplication, QMainWindow


class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui_main_window = Ui_MainWindow()
        self.ui_main_window.setupUi(self)
        self.setWindowTitle("DROITEREG")
        self.setWindowIcon(QIcon(df.ressource_path('icon_droitereg.ico')))

        df.fillAdjustTableWidget(self.ui_main_window.tableWidget_data)

        self.ui_main_window.pushButton_remplissage.clicked.connect(lambda: df.remplissage(self))
        self.ui_main_window.pushButton_droitereg.clicked.connect(lambda: df.droitereg(self))
        self.ui_main_window.pushButton_zero.clicked.connect(lambda: df.zero(self))
        self.ui_main_window.pushButton_print.clicked.connect(lambda: df.print(self))

        self.ui_main_window.tableWidget_data.installEventFilter(self)

    def eventFilter(self, source, event):
        if source == self.ui_main_window.tableWidget_data:
            # Entrée : aller à la cellule en dessous
            if event.type() == QtCore.QEvent.Type.KeyPress:
                if event.key() in (QtCore.Qt.Key.Key_Return, QtCore.Qt.Key.Key_Enter):
                    current = self.ui_main_window.tableWidget_data.currentIndex()
                    nextIndex = current.sibling(current.row() + 1, current.column())
                    if nextIndex.isValid():
                        self.ui_main_window.tableWidget_data.setCurrentIndex(nextIndex)
                        self.ui_main_window.tableWidget_data.edit(nextIndex)
                        return True

                # Coller (Ctrl+V)
                if event.matches(QtGui.QKeySequence.StandardKey.Paste):
                    clipboard = QApplication.clipboard()
                    text = clipboard.text()
                    rows = text.strip().splitlines()

                    start_row = self.ui_main_window.tableWidget_data.currentRow()
                    start_col = self.ui_main_window.tableWidget_data.currentColumn()

                    for i, row in enumerate(rows):
                        # On gère les séparateurs tabulation ou point-virgule
                        columns = [c.strip() for c in row.split('\t')]
                        if len(columns) == 1:
                            columns = [c.strip() for c in row.split(';')]
                        for j, cell in enumerate(columns):
                            target_row = start_row + i
                            target_col = start_col + j
                            if (target_row < self.ui_main_window.tableWidget_data.rowCount() and
                                target_col < self.ui_main_window.tableWidget_data.columnCount()):
                                self.ui_main_window.tableWidget_data.setItem(
                                    target_row, target_col,
                                    df.makeTableItem(cell)
                                )
                    return True

        return super().eventFilter(source, event)

def main():
    app = QApplication([])
    window = Window()
    window.show()
    app.exec()

if __name__ == "__main__":
    main()
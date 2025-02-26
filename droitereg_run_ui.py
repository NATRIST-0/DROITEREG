from PyQt6.QtWidgets import QApplication, QMainWindow
from droitereg_ui import Ui_MainWindow
import droitereg_fonctions as df

class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        # Initialisation de l'interface graphique
        self.ui_main_window = Ui_MainWindow()
        self.ui_main_window.setupUi(self)
        self.setWindowTitle("Régression Linéaire")
        self.resize(1344, 804)  # Redimensionne la fenêtre

        # Ajuster la taille du tableau (si nécessaire)
        df.adjustTableWidgetSize(self.ui_main_window.tableWidget_data)

        # Connexion des boutons aux fonctions
        self.ui_main_window.pushButton_droitereg.clicked.connect(lambda: df.droitereg(self))
        self.ui_main_window.pushButton_zero.clicked.connect(lambda: df.zero(self))
        #self.ui_main_window.pushButton_print.clicked.connect(lambda: df.print(self))

if __name__ == "__main__":
    app = QApplication([])
    window = Window()
    window.show()
    app.exec()
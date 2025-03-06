import os
import sys
from pathlib import Path
from PyQt6.QtGui import QIcon
import droitereg_fonctions as df
from droitereg_ui import Ui_MainWindow
from PyQt6.QtWidgets import QApplication, QMainWindow

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

current_dir = Path(os.path.dirname(os.path.abspath(__file__)))

icon_file = resource_path('icon_droitereg.svg')

class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        # Initialisation de l'interface graphique
        self.ui_main_window = Ui_MainWindow()
        self.ui_main_window.setupUi(self)
        self.setWindowTitle("Régression Linéaire")
        self.setWindowIcon(QIcon(icon_file))  # Ajoute une icône à la fenêtre 

        # Variable pour suivre l'état du thème
        self.is_dark_theme = True
        # Appliquer le thème sombre par défaut
        df.dark_theme(self)

        # Ajuster la taille du tableau (si nécessaire)
        df.adjustTableWidgetSize(self.ui_main_window.tableWidget_data)

        #Ajuster la taille du label_signature
        self.ui_main_window.label_signature.setStyleSheet("font-size: 5pt;")
        self.ui_main_window.pushButton_light_mode.setIcon(QIcon(resource_path('icon_sun_moon.png')))

        # Connexion des boutons aux fonctions
        self.ui_main_window.pushButton_droitereg.clicked.connect(lambda: df.droitereg(self))
        self.ui_main_window.pushButton_zero.clicked.connect(lambda: df.zero(self))
        self.ui_main_window.pushButton_print.clicked.connect(lambda: df.print(self))
        self.ui_main_window.pushButton_light_mode.clicked.connect(lambda: df.light_mode(self))
        self.ui_main_window.pushButton_remplissage.clicked.connect(lambda: df.remplissage(self))


if __name__ == "__main__":
    app = QApplication([])
    window = Window()
    window.show()
    app.exec()
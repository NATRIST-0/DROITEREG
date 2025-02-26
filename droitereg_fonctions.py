"""
Régression Linéraire - Fonctions
"""
import numpy as np
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from PyQt6 import QtWidgets

def droitereg(self):
    # Récupération des données
    data = self.ui_main_window.tableWidget_data
    
    # Initialize default values
    label_x = QtWidgets.QTableWidgetItem("X")
    label_y = QtWidgets.QTableWidgetItem("Y")
    unite_x = QtWidgets.QTableWidgetItem("[]")
    unite_y = QtWidgets.QTableWidgetItem("[]")

    # Try to get actual values if they exist
    if data.item(0, 0): label_x = data.item(0, 0)
    if data.item(0, 1): label_y = data.item(0, 1)
    if data.item(1, 0): unite_x = data.item(1, 0)
    if data.item(1, 1): unite_y = data.item(1, 1)


    # Récupération des valeurs de X et Y
    x = []
    y = []
    # X commence à partir de 3,3 et Y à partir de 3,4
    for i in range(2, data.rowCount()):
        item_x = data.item(i, 0)
        item_y = data.item(i, 1)
        if item_x and item_y and item_x.text() and item_y.text():
            try:
                x.append(float(item_x.text()))
                y.append(float(item_y.text()))
            except ValueError:
                continue
    x = np.array(x)
    y = np.array(y)

    # Régression linéaire
    a, b = np.polyfit(x, y, 1)
    y_reg = a * x + b
    r_carre=1-np.sum((y-y_reg)**2)/np.sum((y-np.mean(y))**2)

    # Remplissage des données Y corrigées et Écart, ycorigées recalculé avec y=mx+p, Ycor colonne 2 et Écart colonne 3
    for i in range(2, data.rowCount()):
        item_x = data.item(i, 0)
        if item_x and item_x.text():
            try:
                x_val = float(item_x.text())
                y_cor = a * x_val + b
                y_val = float(data.item(i, 1).text()) if data.item(i, 1) and data.item(i, 1).text() else 0
                ecart = y_val - y_cor
                
                data.setItem(i, 2, QtWidgets.QTableWidgetItem(f"{y_cor:.2f}"))
                data.setItem(i, 3, QtWidgets.QTableWidgetItem(f"{ecart:.2f}"))
            except ValueError:
                continue


    # Affichage dans le graphe graph_layout QWidget    
    # Create figure and canvas
    fig = Figure()
    canvas = FigureCanvas(fig)
    ax = fig.add_subplot(111)
    
    # Plot data
    ax.scatter(x, y, color='dodgerblue', label=f'y={a:.2f}x+{b:.2f}\nR²={r_carre:.2f}\nx=(y-b)/a')
    ax.plot(x, y_reg, color='crimson')
    ax.set_title(f'Régression Linéaire de {label_y.text()} en fonction de {label_x.text()}')
    ax.set_xlabel(f'{label_x.text()} ({unite_x.text()})')
    ax.set_ylabel(f'{label_y.text()} ({unite_y.text()})')
    ax.legend()
    ax.grid()
    
    # Clear existing layout and add new canvas
    layout = QtWidgets.QVBoxLayout(self.ui_main_window.graph_layout)
    layout.addWidget(canvas)



def zero(self):
    # Efface les données
    data = self.ui_main_window.tableWidget_data
    data.clearContents()

    # Efface le graphe
    layout = self.ui_main_window.graph_layout.layout()
    if layout:
        for i in reversed(range(layout.count())):
            layout.itemAt(i).widget().setParent(None)

def adjustTableWidgetSize(tableWidget_data):
    # Calculer la taille optimale de la table
    row_count = tableWidget_data.model().rowCount()
    column_count = tableWidget_data.model().columnCount()

    # Ajuster la taille du widget en fonction de la taille des cellules
    table_width = 0
    table_height = 0

    for col in range(column_count):
        table_width += tableWidget_data.columnWidth(col)

    for row in range(row_count):
        table_height += tableWidget_data.rowHeight(row)

    # Ajouter des marges si nécessaire
    table_width += 76  # Pour les bords et le défilement horizontal
    table_height += 27  # Pour les bords et le défilement vertical

    # Redimensionner le widget de la table
    tableWidget_data.setFixedSize(table_width, table_height)

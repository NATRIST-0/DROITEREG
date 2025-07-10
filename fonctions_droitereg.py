"""
DROITEREG - Fonctions
"""

import os
import io
import sys
import numpy as np
from reportlab.lib import colors
from PyQt6 import QtWidgets,QtCore
from matplotlib.figure import Figure
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from PyQt6.QtWidgets import QFileDialog, QTableWidgetItem
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer

def ressource_path(relative_path):
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

def makeTableItem(value):
    item = QTableWidgetItem(str(value))
    item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
    return item

def print(self):
    # Vérifier si le tableau est vide
    if self.ui_main_window.tableWidget_data.rowCount() < 3 or self.ui_main_window.tableWidget_data.columnCount() < 2:
        QtWidgets.QMessageBox.warning(self, "Erreur", "Le tableau est vide. Remplissez-le avant de générer un PDF.")
        return

    # Vérifier si le graphique est vide
    if not self.ui_main_window.graph_layout.layout() or self.ui_main_window.graph_layout.layout().count() == 0:
        QtWidgets.QMessageBox.warning(self, "Erreur", "Aucun graphique n'est affiché. Effectuez une régression linéaire avant de générer un PDF.")
        return

    # Print le graphe et toutes les données du tableWidget dans un fichier PDF    
    # Demander à l'utilisateur où sauvegarder le PDF
    fileName, _ = QFileDialog.getSaveFileName(
        None,  
        "Enregistrer l'annexe",
        os.path.expanduser("~/Desktop"),
        "Fichiers PDF (*.pdf)"
    )
    
    if not fileName:
        return  
    
    if not fileName.endswith('.pdf'):
        fileName += '.pdf'
    
    # Créer un document PDF
    doc = SimpleDocTemplate(
        fileName,
        pagesize=A4,
        rightMargin=72,
        leftMargin=72,
        topMargin=72,
        bottomMargin=72
    )
    
    elements = []
    styles = getSampleStyleSheet()
    
    # Ajouter un titre
    title = Paragraph("Annexe de Régression Linéaire", styles['Title'])
    elements.append(title)
    elements.append(Spacer(1, 12))
    
    # Capturer le graphique
    graph_layout = self.ui_main_window.graph_layout
    if graph_layout and graph_layout.layout() and graph_layout.layout().count() > 0:
        canvas_item = graph_layout.layout().itemAt(0).widget()
        if isinstance(canvas_item, FigureCanvas):
            # Obtenir la figure et la sauvegarder dans un buffer
            fig = canvas_item.figure
            buf = io.BytesIO()
            fig.savefig(buf, format='png', dpi=300, bbox_inches='tight')
            buf.seek(0)
            
            # Convertir le buffer en image pour ReportLab
            from reportlab.lib.utils import ImageReader
            img = ImageReader(buf)
            
            # Calculer les dimensions pour garder le ratio
            img_width = doc.width * 0.8  
            img_height = img_width * (fig.get_figheight() / fig.get_figwidth())
            
            # Ajouter le graphique au PDF comme une image
            elements.append(Paragraph("Graphique de régression:", styles['Heading2']))
            elements.append(Spacer(1, 6))
            from reportlab.platypus import Image
            elements.append(Image(buf, width=img_width, height=img_height))
            elements.append(Spacer(1, 12))
    
    # Obtenir les données du tableau
    table_widget = self.ui_main_window.tableWidget_data
    
    if table_widget:
        elements.append(Paragraph("Données:", styles['Heading2']))
        elements.append(Spacer(1, 6))
        
        # Créer une liste pour stocker les données
        table_data = []
        
        # Créer l'en-tête combiné (label + unité)
        combined_headers = []
        
        for col in range(table_widget.columnCount()):
            header_item = table_widget.item(0, col)
            unit_item = table_widget.item(1, col)
            
            header = header_item.text() if header_item else f"Colonne {col+1}"
            unit = unit_item.text() if unit_item else ""
            
            # Combiner le label et l'unité
            combined_header = f"{header} ({unit})" if unit else header
            combined_headers.append(combined_header)
        
        table_data.append(combined_headers)
        
        # Récupérer les données
        for row in range(2, table_widget.rowCount()):
            row_data = []
            empty_row = True
            
            for col in range(table_widget.columnCount()):
                item = table_widget.item(row, col)
                value = item.text() if item else ""
                row_data.append(value)
                if value:
                    empty_row = False
            
            if not empty_row:
                table_data.append(row_data)
        
        pdf_table = Table(table_data)
        
        table_style = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.dodgerblue),  # First row blue
            ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 6),
            ('BACKGROUND', (0, 1), (-1, 1), colors.white)  # Second row red
        ])
        
        for i in range(2, len(table_data), 2):
            table_style.add('BACKGROUND', (0, i), (-1, i), colors.lightgrey)
        
        pdf_table.setStyle(table_style)
        elements.append(pdf_table)
    
    # Ajouter les commentaires à la fin seulement s'ils existent
    commentaires = self.ui_main_window.textEdit_commentaires.toPlainText().strip()
    if commentaires:
        elements.append(Spacer(1, 30))
        elements.append(Paragraph("Commentaires:", styles['Heading2']))
        elements.append(Paragraph(commentaires, styles['Normal']))

    # Générer le PDF
    doc.build(elements)

def zero(self):
    # Efface les données
    data = self.ui_main_window.tableWidget_data
    commentaires = self.ui_main_window.textEdit_commentaires
    data.clearContents()
    commentaires.clear()

    # Efface le graphe
    layout = self.ui_main_window.graph_layout.layout()
    if layout:
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()
        # Remove the old layout
        QtWidgets.QWidget().setLayout(layout)

def droitereg(self):
    # Récupération des données
    data = self.ui_main_window.tableWidget_data

    # Vérifier si le tableau a au moins 2 colonnes
    if data.columnCount() < 2:
        QtWidgets.QMessageBox.warning(self, "Erreur", "Le tableau doit avoir au moins 2 colonnes (X et Y).")
        return

    # Récupération des étiquettes et unités
    label_x = data.item(0, 0) or QtWidgets.QTableWidgetItem("X")
    label_y = data.item(0, 1) or QtWidgets.QTableWidgetItem("Y")
    unite_x = data.item(1, 0) or QtWidgets.QTableWidgetItem("[]")
    unite_y = data.item(1, 1) or QtWidgets.QTableWidgetItem("[]")

    # Mise à jour des entêtes des colonnes 2 et 3
    data.setItem(0, 2, QtWidgets.QTableWidgetItem(f"{label_x.text()} converti"))
    data.setItem(0, 3, QtWidgets.QTableWidgetItem("Écart"))
    data.setItem(1, 2, QtWidgets.QTableWidgetItem(f"{unite_x.text()}"))
    data.setItem(1, 3, QtWidgets.QTableWidgetItem(f"{unite_x.text()}"))

    # Extraction des données numériques
    x_vals = []
    y_vals = []

    for i in range(2, data.rowCount()):
        item_x = data.item(i, 0)
        item_y = data.item(i, 1)
        if item_x and item_y and item_x.text() and item_y.text():
            try:
                x_vals.append(float(item_x.text()))
                y_vals.append(float(item_y.text()))
            except ValueError:
                QtWidgets.QMessageBox.warning(self, "Erreur", f"Les données à la ligne {i - 1} ne sont pas valides.")
                return

    if len(x_vals) < 2:
        QtWidgets.QMessageBox.warning(self, "Erreur", "Au moins deux points de données valides sont nécessaires.")
        return

    x = np.array(x_vals, dtype=np.float64)
    y = np.array(y_vals, dtype=np.float64)

    # Régression Y = aX + b
    try:
        a, b = np.polyfit(x, y, 1)
        y_reg = a * x + b
        r_carre = 1 - np.sum((y - y_reg) ** 2) / np.sum((y - np.mean(y)) ** 2)
    except Exception as e:
        QtWidgets.QMessageBox.critical(self, "Erreur", f"Erreur lors de la régression linéaire : {str(e)}")
        return

    # Conversion Y → X et calcul de l'écart
    for i in range(2, data.rowCount()):
        item_x = data.item(i, 0)
        item_y = data.item(i, 1)
        if item_x and item_y and item_x.text() and item_y.text():
            try:
                x_mesure = float(item_x.text()) # X - Pression
                y_mesure = float(item_y.text()) # Y - Tension
                x_converti = (y_mesure - b) / a
                ecart = x_mesure - x_converti

                data.setItem(i, 2, QtWidgets.QTableWidgetItem(f"{x_converti:.3f}"))
                data.setItem(i, 3, QtWidgets.QTableWidgetItem(f"{ecart:.3f}"))
            except ValueError:
                continue

    # Affichage du graphe dans le layout
    try:
        fig = Figure()
        canvas = FigureCanvas(fig)
        ax = fig.add_subplot(111)

        ax.scatter(x, y, color='dodgerblue', label=f'y = {a:.4f}x + {b:.4f}\nR² = {r_carre:.4f}')
        ax.plot(x, y_reg, color='crimson')
        ax.set_title(f'{label_y.text()} en fonction de {label_x.text()}')
        ax.set_xlabel(f'{label_x.text()} ({unite_x.text()})')
        ax.set_ylabel(f'{label_y.text()} ({unite_y.text()})')
        ax.grid()
        ax.legend()
        fig.tight_layout()
        fig.patch.set_linewidth(2)
        fig.patch.set_edgecolor('dimgray')

        layout = QtWidgets.QVBoxLayout(self.ui_main_window.graph_layout)
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()
        layout.addWidget(canvas)

    except Exception as e:
        QtWidgets.QMessageBox.critical(self, "Erreur", f"Erreur lors de l'affichage du graphique : {str(e)}")


def fillAdjustTableWidget(tableWidget_data):
    # En-têtes de colonnes
    headers = ["Entrée", "Sortie", "Sortie\nconvertie", "Écart"]
    tableWidget_data.setColumnCount(len(headers))
    tableWidget_data.setHorizontalHeaderLabels(headers)

    # Générer les lignes : "Labels", "Unités", puis 18 lignes numériques
    lignes = 82
    row_labels = ["Labels", "Unités"] + [str(i + 1) for i in range(lignes - 2)]
    tableWidget_data.setRowCount(lignes)
    tableWidget_data.setVerticalHeaderLabels(row_labels)

    # Remplissage initial (vide)
    for row in range(lignes):
        for col in range(len(headers)):
            tableWidget_data.setItem(row, col, QtWidgets.QTableWidgetItem(""))

    hauteur_lignes = 30  # Hauteur des lignes en pixels
    largeur_colonnes = 115  # Largeur des colonnes en pixels

    # Fixer hauteur des lignes à 30 px
    for row in range(lignes):
        tableWidget_data.setRowHeight(row, hauteur_lignes)

    # Fixer largeur des colonnes à 80 px
    for col in range(len(headers)):
        tableWidget_data.setColumnWidth(col, largeur_colonnes)

    # Scroll vertical actif, scroll horizontal désactivé
    tableWidget_data.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAsNeeded)
    tableWidget_data.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

    # Taille fixe uniquement sur la largeur (hauteur peut défiler)
    total_width = tableWidget_data.verticalHeader().width()
    for col in range(tableWidget_data.columnCount()):
        total_width += tableWidget_data.columnWidth(col)
    total_width += 70  # marges ou bordures

    # Hauteur d’affichage visible sans scroll : par exemple 25 lignes * 30px + en-tête
    visible_rows = 23  # nombre de lignes visibles sans scroll (modifiable)
    total_height = tableWidget_data.horizontalHeader().height() + (hauteur_lignes * visible_rows)

    tableWidget_data.setFixedSize(total_width, total_height)

def remplissage(self):
    # La fonction remplissage permet de remplir automatiquement les colonnes 0 et 1 avec des valeurs prédéfinis pour tester le programme
    data = self.ui_main_window.tableWidget_data

    data.setItem(0, 0, QtWidgets.QTableWidgetItem("Pression"))
    data.setItem(0, 1, QtWidgets.QTableWidgetItem("Tension"))
    data.setItem(1, 0, QtWidgets.QTableWidgetItem("barA"))
    data.setItem(1, 1, QtWidgets.QTableWidgetItem("V"))
                 
    # Remplissage des données
    data.setItem(2, 0, QtWidgets.QTableWidgetItem("0.332"))
    data.setItem(2, 1, QtWidgets.QTableWidgetItem("1.239"))
    data.setItem(3, 0, QtWidgets.QTableWidgetItem("0.548"))
    data.setItem(3, 1, QtWidgets.QTableWidgetItem("2.105"))
    data.setItem(4, 0, QtWidgets.QTableWidgetItem("1.013"))
    data.setItem(4, 1, QtWidgets.QTableWidgetItem("3.962"))
    data.setItem(5, 0, QtWidgets.QTableWidgetItem("1.513"))
    data.setItem(5, 1, QtWidgets.QTableWidgetItem("5.972"))
    data.setItem(6, 0, QtWidgets.QTableWidgetItem("2.013"))
    data.setItem(6, 1, QtWidgets.QTableWidgetItem("7.960"))
    data.setItem(7, 0, QtWidgets.QTableWidgetItem("2.513"))
    data.setItem(7, 1, QtWidgets.QTableWidgetItem("9.970"))
    # Ajout d'un commentaire
    commentaires = self.ui_main_window.textEdit_commentaires
    commentaires.setPlainText("Mesures effectuées avec multimètre EC1469")

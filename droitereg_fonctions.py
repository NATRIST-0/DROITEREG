"""
Régression Linéraire - Fonctions
"""
import numpy as np
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from PyQt6 import QtWidgets
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
import io
import os
from PyQt6.QtWidgets import QFileDialog

def print(self):
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

    # Compléter les labels et unités des colonnes 2 et 3
    data.setItem(0, 2, QtWidgets.QTableWidgetItem(f"{label_y.text()} corrigé"))
    data.setItem(0, 3, QtWidgets.QTableWidgetItem("Écart"))
    data.setItem(1, 2, QtWidgets.QTableWidgetItem(f"{unite_y.text()}"))
    data.setItem(1, 3, QtWidgets.QTableWidgetItem(f"{unite_y.text()}"))


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
    ax.scatter(x, y, color='dodgerblue', label=f'y={a:.3f}x+{b:.3f}\nR²={r_carre:.3f}')
    ax.plot(x, y_reg, color='crimson')
    ax.set_title(f'Régression Linéaire de {label_y.text()} en fonction de {label_x.text()}')
    ax.set_xlabel(f'{label_x.text()} ({unite_x.text()})')
    ax.set_ylabel(f'{label_y.text()} ({unite_y.text()})')
    ax.legend()
    ax.grid()
    fig.patch.set_linewidth(2)
    fig.patch.set_edgecolor('dimgray')
    fig.subplots_adjust(top=0.91, bottom=0.11, left=0.06, right=0.95, hspace=0.2, wspace=0.3)

    
    # Clear existing layout and add new canvas
    layout = QtWidgets.QVBoxLayout(self.ui_main_window.graph_layout)
    layout.addWidget(canvas)

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
    table_height += 38  # Pour les bords et le défilement vertical

    # Redimensionner le widget de la table
    tableWidget_data.setFixedSize(table_width, table_height)

    # Bloquer les colonnes 2 et 3 pour ne pas pouvoir écrire dedans

def remplissage(self):
    # La fonction remplissage permet de remplir automatiquement les colonnes 0 et 1 avec des valeurs prédéfinis pour tester le programme
    # Compléter les labels et unités des colonnes 0 et 1
    data = self.ui_main_window.tableWidget_data

    data.setItem(0, 1, QtWidgets.QTableWidgetItem("Tension"))
    data.setItem(0, 0, QtWidgets.QTableWidgetItem("Force"))
    data.setItem(1, 1, QtWidgets.QTableWidgetItem("V"))
    data.setItem(1, 0, QtWidgets.QTableWidgetItem("kN"))
                 
    # Remplissage des données
    data.setItem(2, 0, QtWidgets.QTableWidgetItem("0"))
    data.setItem(2, 1, QtWidgets.QTableWidgetItem("0.5"))
    data.setItem(3, 0, QtWidgets.QTableWidgetItem("1"))
    data.setItem(3, 1, QtWidgets.QTableWidgetItem("1.4"))
    data.setItem(4, 0, QtWidgets.QTableWidgetItem("2"))
    data.setItem(4, 1, QtWidgets.QTableWidgetItem("2.6"))
    data.setItem(5, 0, QtWidgets.QTableWidgetItem("3"))
    data.setItem(5, 1, QtWidgets.QTableWidgetItem("3.5"))
    data.setItem(6, 0, QtWidgets.QTableWidgetItem("4"))
    data.setItem(6, 1, QtWidgets.QTableWidgetItem("4.6"))

    # Ajout d'un commentaire
    commentaires = self.ui_main_window.textEdit_commentaires
    commentaires.setPlainText("Mesures effectuées avec multimètre EC1469")


# Theme for dark mode
def dark_theme(self):
    self.setStyleSheet("""
        QWidget {
            background-color: #2E3440;
            color: #D8DEE9;
            font-family: 'Segoe UI';
            font-size: 12px;
        }
        QPushButton {
            background-color: #4C566A;
            border-radius: 5px;
            padding: 5px 10px;
            font-family: 'Segoe UI';
            font-size: 12px;
        }
        QPushButton:hover {
            background-color: #81A1C1;
        }
        QTableWidget {
            background-color: #3B4252;
            color: #D8DEE9;
            gridline-color: #4C566A;
            font-family: 'Segoe UI';
            font-size: 12px;
        }
        QTableWidget::item {
            padding: 5px;
        }
        QTableWidget::item:selected {
            background-color: #FFC107;
        }
        QHeaderView::section:horizontal {
            gridline-color: #4C566A;        
            padding: 5px;
            background-color: #4C566A;
            font-family: 'Segoe UI';
            font-size: 12px;
        }
        QHeaderView::section:horizontal:checked {
            background-color: #5E81AC;
        }
        QHeaderView::section:horizontal:pressed {
            background-color: #81A1C1;
        }
        QToolTip {
            background-color: #4C566A;
            color: #D8DEE9;
            border: 1px solid #D8DEE9;
            font-family: 'Segoe UI';
            font-size: 12px;
        }
    """)

# Theme for light mode
def light_theme(self):
    self.setStyleSheet("""
        QWidget {
            background-color: #FFFFFF;  /* Fond blanc */
            color: #000000;            /* Texte noir */
            font-family: 'Segoe UI';
            font-size: 12px;
        }
        QPushButton {
            background-color: #007BFF;  /* Boutons bleus */
            color: #FFFFFF;             /* Texte blanc */
            border-radius: 5px;
            padding: 5px 10px;
            font-family: 'Segoe UI';
            font-size: 12px;
        }
        QPushButton:hover {
            background-color: #0056B3;  /* Bleu plus foncé au survol */
        }
        QTableWidget {
            background-color: #FFFFFF;  /* Fond blanc */
            color: #000000;            /* Texte noir */
            gridline-color: #DDDDDD;    /* Bordures grises */
            font-family: 'Segoe UI';
            font-size: 12px;
        }
        QTableWidget::item {
            padding: 5px;
        }
        QTableWidget::item:selected {
            background-color: #FFC107;  /* Jaune pour les éléments sélectionnés */
        }
        QHeaderView::section:horizontal {
            background-color: #E9ECEF;  /* En-têtes gris clair */
            color: #000000;             /* Texte noir */
            padding: 5px;
            font-family: 'Segoe UI';
            font-size: 12px;
        }
        QHeaderView::section:horizontal:checked {
            background-color: #B3D7FF;  /* Bleu pastel pour les en-têtes sélectionnés */
        }
        QToolTip {
            background-color: #FFFFFF;  /* Fond blanc */
            color: #000000;            /* Texte noir */
            border: 1px solid #CCCCCC; /* Bordure grise */
            font-family: 'Segoe UI';
            font-size: 12px;
        }
    """)

def light_mode(self):
    if self.is_dark_theme:
        light_theme(self)
        self.is_dark_theme = False
    else:
        dark_theme(self)
        self.is_dark_theme = True
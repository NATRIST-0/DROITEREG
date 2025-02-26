from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
import matplotlib.pyplot as plt
import numpy as np
import io

# Créer un graphique matplotlib
def create_matplotlib_graph():
    # Exemple de données
    x = np.linspace(0, 10, 100)
    y = np.sin(x)
    
    # Créer une figure et un axe
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.plot(x, y)
    ax.set_title("Courbe Sinusoïdale")
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.grid(True)
    
    # Sauvegarder la figure dans un buffer (pas besoin de fichier temporaire)
    buf = io.BytesIO()
    plt.savefig(buf, format='png', dpi=300, bbox_inches='tight')
    buf.seek(0)
    
    # Fermer la figure pour libérer la mémoire
    plt.close(fig)
    
    return buf

# Créer un PDF avec le graphique matplotlib
def create_pdf_with_graph(pdf_path):
    # Créer un nouveau fichier PDF
    c = canvas.Canvas(pdf_path)
    
    # Ajouter du texte
    c.drawString(100, 750, "Test impression PDF avec graphique matplotlib")
    
    # Créer et ajouter le graphique
    graph_buffer = create_matplotlib_graph()
    img = ImageReader(graph_buffer)
    
    # Positionner et dimensionner l'image dans le PDF
    c.drawImage(img, 100, 400, width=400, height=300)
    
    # Ajouter un tableau de données (exemple simple avec des rectangles)
    data = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    
    # Position et dimensions du tableau
    table_x = 100
    table_y = 300
    cell_width = 50
    cell_height = 30
    
    # Dessiner le tableau
    for i, row in enumerate(data):
        for j, value in enumerate(row):
            # Calculer la position de la cellule
            x = table_x + (j * cell_width)
            y = table_y - (i * cell_height)
            
            # Dessiner le rectangle de la cellule
            c.rect(x, y, cell_width, cell_height)
            
            # Ajouter le texte de la cellule
            c.drawString(x + 20, y + 10, str(value))
    
    # Ajouter un texte descriptif
    c.drawString(100, 250, "Tableau de données et graphique générés avec Python")
    
    # Sauvegarder le PDF
    c.save()

# Appeler la fonction avec le chemin de votre PDF
create_pdf_with_graph(r"C:\Users\GAYRARD\Desktop\exemple_avec_graphique.pdf")
# Bibliothèque pandas
import pandas as pd
# Importation de la bibliothèque de visualisation
import matplotlib.pyplot as plt
# Bibliothèque mathématique
import numpy as np

# Fonction pour créer une connexion et un curseur vers la base de données
def make_connection_with_db():
    import mysql.connector  # Bibliothèque de connexion MySQL
    connection_mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="wp-ecommerce"
    )
    cursor = connection_mydb.cursor(dictionary=True)
    return connection_mydb, cursor

# Fonction pour récupérer le total des quantités vendues par catégorie de produits
def get_categories_sales():
    _, cursor = make_connection_with_db()
    
    # Requête SQL pour récupérer les ventes par catégorie de produits
    sql = '''
    SELECT wp_term_taxonomy.term_id, wp_terms.name,   
           SUM(wp_wc_order_product_lookup.product_qty) AS sumsales
    FROM wp_wc_order_product_lookup 
    INNER JOIN wp_term_relationships  
        ON wp_term_relationships.object_id = wp_wc_order_product_lookup.product_id
    INNER JOIN wp_term_taxonomy 
        ON wp_term_relationships.term_taxonomy_id = wp_term_taxonomy.term_taxonomy_id
    INNER JOIN wp_terms 
        ON wp_terms.term_id = wp_term_taxonomy.term_id
    WHERE wp_term_taxonomy.taxonomy = 'product_cat' 
    GROUP BY wp_term_taxonomy.term_id
    '''
    cursor.execute(sql)
    results = cursor.fetchall()

    # Création d'un DataFrame vide pour stocker les résultats
    df = pd.DataFrame(columns=['category_id', 'Category', 'Sales'])

    # Parcours des résultats de la requête
    for row in results:
        category_id = row['term_id']         # ID de la catégorie
        Category = row['name']               # Nom de la catégorie
        Sales = row['sumsales']              # Quantité totale vendue
        # Création d’un dictionnaire temporaire
        obj = {
            "category_id": [category_id],
            "Category": [Category],
            "Sales": [Sales]
        }
        df_obj = pd.DataFrame(obj)
        # Ajout de la ligne au DataFrame
        df = pd.concat([df, df_obj], ignore_index=True)
    
    return df

# Fonction pour afficher un diagramme à barres des ventes par catégorie
def show_customers_by_countries_bars():
    df = get_categories_sales()
    
    # Bibliothèques pour un affichage correct de l’arabe
    import arabic_reshaper
    from bidi.algorithm import get_display

    # Conversion des noms de catégories en arabe affichable correctement
    df['Category'] = df['Category'].apply(lambda a: get_display(arabic_reshaper.reshape(a)))

    # Préparation des axes
    x = df['Category']  # Axe des catégories
    y = df['Sales']     # Axe des ventes

    # Taille du graphique
    plt.figure(figsize=(10, 6))
    plt.xlabel("Catégorie")
    plt.ylabel("Ventes")
    plt.title('Ventes par catégorie')

    # Couleurs aléatoires pour les barres
    colors = []
    for i in range(len(x)):
        colors.append([np.random.rand(), np.random.rand(), np.random.rand()])
        # Affichage de la valeur sur chaque barre
        plt.text(x=i, y=y[i], s=y[i])

    # Dessin du graphique à barres
    plt.bar(x, y, color=colors)
    plt.show()

# Appel de la fonction pour afficher le graphique
show_customers_by_countries_bars()

# Bibliothèque pandas
import pandas as pd
# Importation de la bibliothèque de visualisation
import matplotlib.pyplot as plt

# Fonction pour établir une connexion et obtenir un curseur vers la base de données
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

    # Requête SQL pour calculer les ventes par catégorie
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

    cursor.execute(sql)             # Exécution de la requête
    results = cursor.fetchall()     # Récupération des résultats

    # Création d’un DataFrame vide pour stocker les données
    df = pd.DataFrame(columns=['category_id', 'Category', 'Sales'])

    # Parcours des résultats pour remplir le DataFrame
    for row in results:
        category_id = row['term_id']        # ID de la catégorie
        Category = row['name']              # Nom de la catégorie
        Sales = row['sumsales']             # Total des quantités vendues

        obj = {
            "category_id": [category_id],
            "Category": [Category],
            "Sales": [Sales]
        }
        df_obj = pd.DataFrame(obj)
        df = pd.concat([df, df_obj], ignore_index=True)  # Ajout au DataFrame principal
    
    return df

# Fonction pour afficher un graphique en camembert des ventes par catégorie
def show_categories_sales_pie():
    df = get_categories_sales()  # Récupération des données

    # Bibliothèques pour l'affichage correct de l'arabe
    import arabic_reshaper
    from bidi.algorithm import get_display

    # Adaptation des noms de catégories pour un affichage correct en arabe
    df['Category'] = df['Category'].apply(lambda a: get_display(arabic_reshaper.reshape(a)))

    # Taille de la figure
    plt.figure(figsize=(10, 6))

    # Dessin du graphique en camembert
    plt.pie(df['Sales'], labels=df['Category'], autopct='%1.1f%%')

    # Titre du graphique
    plt.title('Répartition des ventes par catégorie')

    # Affichage du graphique
    plt.show()

# Appel de la fonction pour afficher le graphique
show_categories_sales_pie()

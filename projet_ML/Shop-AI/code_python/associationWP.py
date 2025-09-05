# Bibliothèque de connexion à la base de données
import mysql.connector

# Déclaration de variables globales pour la connexion et le curseur
connection_mydb = None
cursor = None

# Fonction pour établir la connexion avec la base de données
def mysql_connect():
    global cursor, connection_mydb
    connection_mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="wp-ecommerce"
    )
    # Création du curseur avec résultats sous forme de dictionnaire
    cursor = connection_mydb.cursor(dictionary=True)

# Fonction pour récupérer le nom d’un produit à partir de son identifiant
def get_product_name_from_id(connection_mydb, product_id):
    cursor = connection_mydb.cursor(dictionary=True)
    sql = "SELECT * FROM wp_posts WHERE ID=(%s)"
    id = (product_id, )
    cursor.execute(sql, id)
    results = cursor.fetchall()
    if len(results) > 0:
        return results[0]['post_title']
    return "Produit Inconnu"

# Bibliothèque pandas
import pandas as pd

# Fonction pour construire le DataFrame des produits associés
def build_dataframe_associated_products(connection_mydb):
    df = pd.DataFrame(columns=[0,1,2,3,4,5,6,7,8,9])
    cursor = connection_mydb.cursor(dictionary=True)
    
    # Requête pour obtenir toutes les commandes
    sql = "SELECT * FROM wp_wc_order_stats ORDER BY order_id"
    cursor.execute(sql)
    results_orders = cursor.fetchall()

    # Parcours de chaque commande
    for order in results_orders:
        order_id = order['order_id']
        sql = "SELECT * FROM wp_wc_order_product_lookup WHERE order_id=(%s)"
        id = (order_id,)
        cursor.execute(sql, id)
        results_products = cursor.fetchall()
        
        products_ids = []
        for product in results_products:
            product_id = product['product_id']
            if product_id > 0:
                products_ids.append(product_id)
        
        # Ajout au DataFrame si plus d’un produit dans la commande
        if len(products_ids) > 1:
            df = pd.concat([df, pd.DataFrame([products_ids])], ignore_index=True)
    
    return df

# Fonction pour préparer les transactions à partir du DataFrame
def prepare_transactions(df):
    df = df.T  # Transposition du DataFrame
    transactions = df.apply(lambda x: x.dropna().tolist())  # Suppression des valeurs nulles
    transactions_list = transactions.tolist()
    
    # Encodage des transactions
    from mlxtend.preprocessing import TransactionEncoder
    te = TransactionEncoder()
    te_model = te.fit(transactions_list)
    rows = te_model.transform(transactions_list)
    df_transactions = pd.DataFrame(rows, columns=te_model.columns_)
    return df_transactions

# Fonction pour générer les règles d'association
def generate_association_rules(df_transactions, min_support, min_confidence):
    from mlxtend.frequent_patterns import apriori
    frequent_itemsets = apriori(df_transactions, min_support=min_support, use_colnames=True)
    
    from mlxtend.frequent_patterns import association_rules
    rules = association_rules(frequent_itemsets, metric="confidence", min_threshold=min_confidence)
    rules = rules.sort_values(['confidence'], ascending=[False])
    return rules

# Fonction pour exporter les règles vers la base de données
def export_to_db(connection_mydb, rules):
    cursor = connection_mydb.cursor()
    
    # Suppression de la table si elle existe
    sql = "DROP TABLE IF EXISTS custom_products_association"
    cursor.execute(sql)
    
    # Création de la table
    sql = '''
    CREATE TABLE custom_products_association (
        ID int(11) NOT NULL AUTO_INCREMENT,
        product_id_in int(11) NOT NULL,
        post_title_in text NOT NULL,
        product_id_out int(11) NOT NULL,
        post_title_out text NOT NULL,
        confidence double NOT NULL,
        PRIMARY KEY (ID)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
    '''
    cursor.execute(sql)
    connection_mydb.commit()
    
    # Insertion des règles
    for row in rules.itertuples():
        antecedents = row.antecedents
        consequents = row.consequents
        confidence = row.confidence * 100
        
        for product1 in antecedents:
            post_title_in = get_product_name_from_id(connection_mydb, product1)
            for product2 in consequents:
                post_title_out = get_product_name_from_id(connection_mydb, product2)
                
                # Suppression des anciennes entrées avec une confiance plus faible
                sql = '''DELETE FROM custom_products_association 
                         WHERE product_id_in=(%s) AND product_id_out=(%s) AND confidence <= (%s)'''
                params = (product1, product2, confidence)
                cursor.execute(sql, params)
                
                # Vérification d'existence d'une règle avec une meilleure confiance
                sql = '''SELECT * FROM custom_products_association 
                         WHERE product_id_in=(%s) AND product_id_out=(%s) AND confidence >= (%s)'''
                params = (product1, product2, confidence)
                cursor.execute(sql, params)
                results = cursor.fetchall()
                
                must_add = True
                if results is not None and len(results) > 0:
                    must_add = False
                
                # Ajout de la règle si elle n’existe pas
                if must_add:
                    sql = '''INSERT INTO custom_products_association 
                             (product_id_in, post_title_in, product_id_out, post_title_out, confidence) 
                             VALUES (%s, %s, %s, %s, %s)'''
                    val = (product1, post_title_in, product2, post_title_out, confidence)
                    cursor.execute(sql, val)
                    connection_mydb.commit()

# Fonction principale de lancement
def start_generate_association_rules():
    mysql_connect()
    df = build_dataframe_associated_products(connection_mydb)
    transactions_df = prepare_transactions(df)
    
    min_support = 0.001
    min_confidence = 0.001
    
    rules = generate_association_rules(transactions_df, min_support, min_confidence)
    export_to_db(connection_mydb, rules)
    connection_mydb.close()

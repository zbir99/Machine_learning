# Importation de la bibliothèque pandas pour manipuler les données
import pandas as pd

# Fonction pour se connecter à la base de données MySQL
def make_connection_with_db():
    import mysql.connector
    # Connexion à la base de données "wp-ecommerce"
    connection_mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="wp-ecommerce"
    )
    # Création d’un curseur pour exécuter les requêtes SQL
    cursor = connection_mydb.cursor(dictionary=True)
    return connection_mydb, cursor

# Fonction pour récupérer les profils des utilisateurs (pays, âge, sexe)
def get_users_profiles():
    # Création d’un DataFrame vide avec les colonnes souhaitées
    df = pd.DataFrame(columns=['user_id', 'country', 'age', 'gender'])
    
    # Connexion à la base de données et récupération du curseur
    _, cursor = make_connection_with_db()
    
    # Requête SQL pour obtenir les ID de tous les utilisateurs
    sql = "SELECT ID FROM wp_users"
    cursor.execute(sql)
    users_results = cursor.fetchall()

    # Parcours de chaque utilisateur
    for user in users_results:
        user_id = user['ID']

        # --- Récupération du pays ---
        sql = "SELECT meta_value FROM wp_usermeta WHERE user_id = %s AND meta_key = 'country'"
        cursor.execute(sql, (user_id,))
        result = cursor.fetchall()
        country = result[0]['meta_value'] if result and len(result) > 0 else "Unknown"

        # --- Récupération de l'âge ---
        sql = "SELECT meta_value FROM wp_usermeta WHERE user_id = %s AND meta_key = 'age'"
        cursor.execute(sql, (user_id,))
        result = cursor.fetchall()
        age = result[0]['meta_value'] if result and len(result) > 0 else "Unknown"

        # --- Récupération du genre ---
        sql = "SELECT meta_value FROM wp_usermeta WHERE user_id = %s AND meta_key = 'gender'"
        cursor.execute(sql, (user_id,))
        result = cursor.fetchall()
        gender = result[0]['meta_value'] if result and len(result) > 0 else "Unknown"

        # Création d’un dictionnaire avec les données de l’utilisateur
        obj = {
            "user_id": [user_id],
            "country": [country],
            "age": [age],
            "gender": [gender]
        }

        # Conversion du dictionnaire en DataFrame et ajout à la table principale
        df_obj = pd.DataFrame(obj)
        df = pd.concat([df, df_obj], ignore_index=True)

    # Suppression des lignes avec des valeurs "Unknown"
    df = df[df['country'] != 'Unknown']
    df = df[df['age'] != 'Unknown']
    df = df[df['gender'] != 'Unknown']

    # Conversion de l’âge en entier (pour analyses numériques)
    df['age'] = pd.to_numeric(df['age'])

    # Retour du DataFrame final
    return df

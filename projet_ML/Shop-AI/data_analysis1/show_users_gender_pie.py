# Importation de la bibliothèque pandas pour manipuler les données
import pandas as pd

# Importation de matplotlib pour les visualisations
import matplotlib.pyplot as plt

# Importation de la fonction qui récupère les profils utilisateurs
from get_users_profiles import get_users_profiles

# Fonction qui affiche un graphique en camembert de la répartition des sexes
def show_users_gender_pie():
    # Récupération des profils utilisateurs sous forme de DataFrame
    df_profile = get_users_profiles()
    
    # Regrouper les données par sexe et compter le nombre d'utilisateurs dans chaque groupe
    df_gender = df_profile[['gender', 'user_id']].groupby('gender').count()

    # Importation de bibliothèques pour bien afficher le texte en arabe
    import arabic_reshaper
    from bidi.algorithm import get_display

    # Réinitialisation de l'index pour faciliter l'accès aux colonnes
    df_gender = df_gender.reset_index()
    
    # Transformation des libellés en arabe pour un affichage correct
    df_gender['gender'] = df_gender['gender'].apply(lambda a: get_display(arabic_reshaper.reshape(a)))
    
    # Création du graphique en camembert
    plt.pie(df_gender['user_id'], labels=df_gender['gender'], autopct='%1.1f%%')
    
    # Titre du graphique
    plt.title('Répartition des utilisateurs selon le sexe')
    
    # Affichage du graphique
    plt.show()

# Appel de la fonction pour afficher le graphique
show_users_gender_pie()

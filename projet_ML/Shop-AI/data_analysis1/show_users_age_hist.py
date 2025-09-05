# Importation de la bibliothèque pandas pour manipuler les données
import pandas as pd

# Importation de matplotlib pour les visualisations
import matplotlib.pyplot as plt

# Importation de la fonction qui récupère les profils des utilisateurs
from get_users_profiles import get_users_profiles

# Fonction pour afficher un histogramme de la répartition des âges des utilisateurs
def show_users_age_hist():
    # Récupération des profils utilisateurs
    df_profile = get_users_profiles()
    
    # Sélection de la colonne "age"
    df_age = df_profile['age']
    
    # Création de l'histogramme avec des intervalles (bins) personnalisés
    df_age.hist(bins=[0, 10, 20, 30, 40, 50, 60, 70, 80])
    
    # Étiquette de l'axe horizontal
    plt.xlabel("Âge")
    
    # Étiquette de l'axe vertical
    plt.ylabel("Nombre d'utilisateurs")
    
    # Titre du graphique
    plt.title("Histogramme des âges des utilisateurs")
    
    # Affichage du graphique
    plt.show()

# Appel de la fonction pour afficher l'histogramme
show_users_age_hist()

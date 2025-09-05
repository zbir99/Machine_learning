# Importation de la bibliothèque pandas pour manipuler les données
import pandas as pd

# Importation de matplotlib pour les visualisations
import matplotlib.pyplot as plt

# Importation de la fonction qui récupère les profils des utilisateurs
from get_users_profiles import get_users_profiles

# Fonction pour afficher un graphique de densité de la répartition des âges
def show_users_age_density():
    # Récupération des profils utilisateurs
    df_profile = get_users_profiles()
    
    # Sélection de la colonne des âges
    df_age = df_profile['age']
    
    # Tracer la courbe de densité des âges
    df_age.plot(kind='density')
    
    # Étiquette de l'axe des x (âge)
    plt.xlabel("Âge")
    
    # Étiquette de l'axe des y (densité de probabilité)
    plt.ylabel("Densité")
    
    # Titre du graphique
    plt.title("Courbe de densité des âges des utilisateurs")
    
    # Affichage du graphique
    plt.show()

# Appel de la fonction pour afficher la courbe de densité
show_users_age_density()

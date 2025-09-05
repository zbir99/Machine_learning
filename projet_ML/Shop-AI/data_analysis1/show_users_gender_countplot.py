# Importation de la bibliothèque pandas pour manipuler les données
import pandas as pd

# Importation de matplotlib pour les visualisations
import matplotlib.pyplot as plt

# Importation de seaborn pour les graphiques améliorés
import seaborn as sns

# Importation de la fonction qui récupère les profils des utilisateurs
from get_users_profiles import get_users_profiles

# Fonction pour afficher un graphique à barres du nombre d'utilisateurs selon le sexe
def show_users_gender_countplot():
    # Importation de bibliothèques pour un affichage correct de l'arabe
    import arabic_reshaper
    from bidi.algorithm import get_display

    # Récupération des profils utilisateurs
    df_profile = get_users_profiles()

    # Définition de la taille de la figure
    plt.subplots(figsize=(8, 6))

    # Titre du graphique
    plt.title("Nombre d'utilisateurs par sexe")

    # Transformation des valeurs du sexe pour un affichage correct en arabe
    df_profile['gender'] = df_profile['gender'].apply(lambda a: get_display(arabic_reshaper.reshape(a)))

    # Création du graphique à barres
    ax = sns.countplot(x=df_profile['gender'])

    # Affichage des valeurs numériques au-dessus des barres
    ax.bar_label(ax.containers[0])

    # Affichage du graphique
    plt.show()

# Appel de la fonction pour afficher le graphique
show_users_gender_countplot()

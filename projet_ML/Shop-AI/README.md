# Shop-AI — Analyses de données e-commerce (WooCommerce)

Ce projet propose des scripts d’analyse et de visualisation autour d’une base WooCommerce (dump SQL fourni), ainsi qu’une génération de règles d’association produit (Apriori) pour des recommandations.

## Sommaire
- Aperçu du projet
- Arborescence
- Pré-requis
- Installation
- Configuration de la base de données
- Utilisation (exécuter les scripts d’analyse)
- Génération des règles d’association
- Notebooks
- Résolution des problèmes (FAQ)
- Licence

## Aperçu du projet
Les scripts accèdent à une base MySQL `wp-ecommerce` (ex: WordPress + WooCommerce) et produisent des visualisations:
- Profils utilisateurs (âge, genre, pays)
- Ventes par catégories de produits
- Répartition des clients par pays
- Règles d’association produits via Apriori (mlxtend)

Le dump SQL `wp-ecommerce.sql` est fourni pour charger des données d’exemple.

## Arborescence
```
projet_ML/Shop-AI/
├─ association_ML/
│  └─ associationWP.ipynb
├─ code_python/
│  └─ associationWP.py                 # Génération règles d’association (Apriori)
├─ data_analysis1/
│  ├─ get_users_profiles.py            # Extraction profils depuis MySQL
│  ├─ show_users_age_density.py        # Densité des âges
│  ├─ show_users_age_hist.py           # Histogramme des âges
│  ├─ show_users_gender_countplot.py   # Barres par genre (ar)
│  └─ show_users_gender_pie.py         # Camembert par genre (ar)
├─ data_analysis2(product sales per category )/
│  ├─ show_categories_sales_bars.py    # Barres des ventes par catégorie (ar)
│  └─ show_categories_sales_pie.py     # Camembert des ventes par catégorie (ar)
├─ data_analysis3(Customer Distribution by Country)/
│  ├─ show_customers_by_countries_bars.py  # Barres clients par pays
│  └─ show_customers_by_countries_pie.py   # Camembert clients par pays
└─ wp-ecommerce.sql
```

## Pré-requis
- Python 3.10+ (testé avec 3.12)
- MySQL Server 8+ (ou compatible)
- Accès local à MySQL (host `localhost`)
- Bibliothèques Python:
  - pandas
  - numpy
  - matplotlib
  - seaborn
  - mysql-connector-python
  - arabic-reshaper
  - python-bidi
  - mlxtend
  - (optionnel) jupyter

Astuce: vous pouvez créer un environnement virtuel et installer:
```
python -m venv .venv
.venv\Scripts\activate
pip install pandas numpy matplotlib seaborn mysql-connector-python arabic-reshaper python-bidi mlxtend jupyter
```

## Installation
1) Cloner / copier ce dossier `Shop-AI` sur votre machine Windows.
2) Créer et activer un venv (voir ci-dessus) puis installer les dépendances.
3) Importer les données dans MySQL (voir section suivante).

## Configuration de la base de données
Les scripts supposent une base MySQL nommée `wp-ecommerce` accessible avec:
- host: `localhost`
- user: `root`
- password: chaîne vide `""`

Si vos identifiants diffèrent, modifiez les fonctions de connexion `make_connection_with_db()` ou `mysql_connect()` dans:
- `data_analysis1/get_users_profiles.py`
- `data_analysis2(product sales per category )/show_categories_sales_bars.py`
- `data_analysis2(product sales per category )/show_categories_sales_pie.py`
- `data_analysis3(Customer Distribution by Country)/show_customers_by_countries_bars.py`
- `data_analysis3(Customer Distribution by Country)/show_customers_by_countries_pie.py`
- `code_python/associationWP.py`

Pour charger le dump d’exemple:
```
mysql -u root -p
CREATE DATABASE IF NOT EXISTS `wp-ecommerce` DEFAULT CHARACTER SET utf8mb4;
USE `wp-ecommerce`;
SOURCE chemin\vers\wp-ecommerce.sql;
```
Sur Windows avec MySQL Shell/Workbench, utilisez l’outil d’import SQL et pointez sur `wp-ecommerce.sql`.

## Utilisation — scripts d’analyse
Important: exécutez les commandes depuis le dossier `Shop-AI/`. Sous Windows, mettez les chemins entre guillemets si nécessaires.

- Âge — densité
```
python "data_analysis1/show_users_age_density.py"
```

- Âge — histogramme
```
python "data_analysis1/show_users_age_hist.py"
```

- Genre — barres (avec rendu arabe)
```
python "data_analysis1/show_users_gender_countplot.py"
```

- Genre — camembert (avec rendu arabe)
```
python "data_analysis1/show_users_gender_pie.py"
```

- Ventes par catégorie — barres (avec rendu arabe)
```
python "data_analysis2(product sales per category )/show_categories_sales_bars.py"
```

- Ventes par catégorie — camembert (avec rendu arabe)
```
python "data_analysis2(product sales per category )/show_categories_sales_pie.py"
```

- Clients par pays — barres
```
python "data_analysis3(Customer Distribution by Country)/show_customers_by_countries_bars.py"
```

- Clients par pays — camembert
```
python "data_analysis3(Customer Distribution by Country)/show_customers_by_countries_pie.py"
```

Chaque script ouvre une fenêtre Matplotlib avec la visualisation correspondante.

## Génération des règles d’association (Apriori)
Le module `code_python/associationWP.py` construit des transactions à partir des commandes WooCommerce, applique Apriori (`mlxtend`) et exporte les règles dans une table MySQL `custom_products_association`.

Paramètres par défaut dans le code:
- `min_support = 0.001`
- `min_confidence = 0.001`

Pour exécuter sans modifier le fichier, lancez depuis `Shop-AI/`:
```
python -c "from code_python.associationWP import start_generate_association_rules; start_generate_association_rules()"
```
À la fin, la table `custom_products_association` est créée et remplie dans `wp-ecommerce`.

## Notebooks
Des notebooks Jupyter sont fournis pour exploration:
- `data_analysis1/analyze_users_profiles.ipynb`
- `data_analysis2(product sales per category )/analyze_categories_sales.ipynb`
- `data_analysis3(Customer Distribution by Country)/analyze_customers_by_countries.ipynb`
- `association_ML/associationWP.ipynb`

Lancez Jupyter:
```
jupyter notebook
```

## Résolution des problèmes (FAQ)
- ImportError: No module named …
  - Activez le venv et `pip install` les dépendances listées plus haut.
- Erreur de connexion MySQL (access denied / timeout)
  - Vérifiez host/user/password et que MySQL est démarré. Adaptez les fonctions de connexion dans les scripts.
- Caractères arabes illisibles dans les graphiques
  - Installez `arabic-reshaper` et `python-bidi` et utilisez une police compatible. Les scripts font déjà le reshape/RTL.
- Graphiques vides
  - Assurez-vous que les tables WooCommerce contiennent des données après import du dump.

## Licence
Ce projet est fourni à des fins éducatives/démonstratives. Ajoutez ici votre licence si nécessaire (MIT, Apache-2.0, etc.).

# Application Flask concernant la base de données Agritox
Pour plus d'informations concernant la base de données, aller sur le site internet suivant : `https://www.data.gouv.fr/fr/datasets/base-de-donnees-agritox/`

Devoir réalisé par Pierre Tuloup dans le cadre du cours Python du Master Technologies appliquées à l'Histoire de l'Ecole nationale des Chartes.

La partie de l'application contenue dans le dossier csv-to-sqlite-main permet d'initialiser et de remplir automatiquement la base de données avec les fichiers csv choisis.

## Setup & Installtion

Une version de Python récente est requise pour l'application (version 3.7 ou plus récente)

```bash
git clone <repo-url>
```

```bash
pip install -r requirements.txt
Suite à des mises à jour de bibliothèques en Flask, je tiens à préciser que le fichier requirements.txt dispose notamment des bibliothèques :
- SQLAlchemy 1.3.23 
- Flask-SQLAlchemy 2.4.4
```

## Running The App

```bash
Lancement : source venv/bin/activate
python3 main.py
```
Une fois l'application lancée, une base de données SQLite test.db est automatiquement générée avec les fichiers CSV choisis (ici Classement, Ecotoxicité, Propriétés physico-chimiques) ainsi que deux tables User et Notes qui stockent les informations des utilisateurs.
Pour le test unitaire, lancer simplement python3 testing.py juste après avoir activé l'environnement virtuel.

## Viewing The App

Aller à `http://127.0.0.1:5000`
L'application dispose de plusieurs fonctionnalités notamment celles du CRUD (Create, Read, Edit, Delete) ainsi que la possibilité de recherche par mot clé grâce à Search.

Par souci d'ergonomie et de mise en application, j'ai choisi de me concentrer sur trois fichiers CSV du dataset du site du gouvernement, concernant le Classement, l'Ecotoxicité ainsi que les Propriétés physico-chimiques des données de la base Agritox.

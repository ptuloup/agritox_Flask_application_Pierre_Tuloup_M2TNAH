from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
import sqlite3
import csv

db = SQLAlchemy() # J'initialise ma base de données SQLite avec SQLAlchemy
DB_NAME = "test.db" # Je nomme ma base de données SQLite "test.db". Elle sera remplie de trois tables provenant de trois fichiers csv trouvés sur data.gouv AGRITOX ; ainsi que d'une table User qui enregistre les utilisateurs du site et d'une table Note pour rajouter des commentaires. Les modifications seront enregistrées dans la base test.db


def create_app():
    app = Flask(__name__) # Initialisation de l'application
    app.config['SECRET_KEY'] = 'hjshjhdjah kjshkjdhjs' # J'entre une clé secrète pour la configuration de ma base de données
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}' # J'entre l'URI qui correspond au chemin relatif vers la base de données
    db.init_app(app) # Cette ligne permet d'executer la fonction de création de l'application.

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/') # Enregistrement d'une fonction blueprint qui indique le chemin vers les fichiers auth.py et views.py
    app.register_blueprint(auth, url_prefix='/') # Enregistrez un plan sur une application avec un préfixe d'URL et / ou un sous-domaine. Les paramètres du préfixe / sous-domaine d'URL deviennent des arguments de vue courants (avec les valeurs par défaut) dans toutes les fonctions de vue du plan.

    from .models import User, Note # Import des tables User et Note pour l'enregistrement des identifiants lors de la connexion ainsi que pour le rajout d'un espace commentaires dans la section Note.

    create_database(app) # Création de la base de données dans l'application.

    login_manager = LoginManager() # Flask-Login fournit la gestion de session utilisateur pour Flask. Il gère les tâches courantes de connexion, de déconnexion et de mémorisation des sessions 
    login_manager.login_view = 'auth.login' # Nom des views à renvoyer quand l'utilisateur doit se connecter.
    login_manager.init_app(app) # Configure une application. Cela enregistre un appel `after_request`, et y attache ce `LoginManager` en tant que` app.login_manager`.

    @login_manager.user_loader # Initialisation de l'utilisateur.
    def load_user(id): # Fonction load_user qui renvoie l'identifiant de l'utilisateur et l'enregistre dans l'application.
        
        return User.query.get(int(id))

    return app

def filltable (tablename,conn):
    arborescence = "./csv-to-sqlite-main/csvfile/" #une variable permettant de reconstruire l'arborescence pour boucler sur les fichiers csv
    with open(arborescence + tablename + ".csv", newline='') as f: #j'ouvre chacun fichier csv
        reader = csv.reader(f, delimiter = ";")
        print('OPEN c bon')
        entete = next(reader) #la fonction next permet ici de récupérer la première ligne de chaque fichier csv où se trouvent les en-têtes
        nombre_colonne = len(entete) #je récupère le nombre de colonnes, cela me servira à initialiser chaque table
        colonnes = ', '.join(entete) #je transforme la liste des en-têtes en une string que je manipulerai pour l'intégrer dans ma requête SQLite
        #les 3 prochaines lignes servent à nettoyer la string pour être acceptable dans une requête SQLite
        colonnes = colonnes.replace("  ", "")
        colonnes = colonnes.replace(" ,", ",")
        colonnes = colonnes.replace("/", "_") #le slash cause une erreur en SQL
        liste_valeur = [] #j'initialise une variable qui sera une liste imbriquée, c'est à dire une liste contenant des listes de toutes les valeurs de chaque ligne
        n = 1 #je crée un index qui correspond à la clé primaire, inexistante dans les fichiers csv
        for row in reader : #je boucle sur le csv pour récupérer chaque ligne et les ajoute à ma liste "liste valeur"
            row = [n] + row #j'ajoute la clé primaire à chaque ligne du csv
            liste_valeur.append(row) #j'ajoute chaque ligne dans ma variable "liste valeur"
            n += 1
        conn.executemany('INSERT INTO {0} VALUES ({1})'.format(tablename,"?," * (int(nombre_colonne)) + "?"), liste_valeur) #Je mets d'un bloc un fichier csv dans une table, car chaque table correspond à un fichier csv


def create_database(app):
    if not path.exists('./website/' + DB_NAME):
        db.create_all(app=app)
        with sqlite3.connect("./website/test.db") as conn:
            print('je rentre ici!!!!!!!!!!!!!!!!!!') #je crée une variable "conn" qui est la connexion de ma base SQLite. A noter que la fonction connect crée automatiquement la base si elle n'existe pas
            cursor = conn.cursor() #permet de créer des requêtes SQLite
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';") #requête SQL permettant de checkez si la base possède déjà des tables
            filltable("Classement",conn)
            filltable("Ecotoxicite",conn)
            filltable("Proprietespc",conn)
        conn.commit()
        conn.close() 
        print('Created Database!')


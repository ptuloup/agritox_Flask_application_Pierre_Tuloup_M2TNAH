import csv, sqlite3, os
from os import path

#tout d'abord, je crée le fichier où doit se trouver la database en vérifiant notamment si elle n'existe déjà pas
if not path.exists("./database/"):
    os.mkdir("./database/")

def filltable (tablename,conn):
    arborescence = "./csvfile/" #une variable permettant de reconstruire l'arborescence pour boucler sur les fichiers csv
    with open(arborescence + tablename + ".csv", newline='') as f: #j'ouvre chacun fichier csv
        reader = csv.reader(f, delimiter = ";")
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
        print(liste_valeur)
        conn.executemany('INSERT INTO {0} VALUES ({1})'.format(tablename,"?," * (int(nombre_colonne)) + "?"), liste_valeur) #Je mets d'un bloc un fichier csv dans une table, car chaque table correspond à un fichier csv


# l'objectif du programme est de créer une base de données appelées "agritox.db" dans le fichier "database". Ensuite, je regarde si la base existe deja ou pas. Si elle existe, ca passe. Si elle n'existe pas, elle va en créer une à partir des fichiers csv déposés dans le dossier "csvfile"
with sqlite3.connect("./database/test.db") as conn: #je crée une variable "conn" qui est la connexion de ma base SQLite. A noter que la fonction connect crée automatiquement la base si elle n'existe pas
    cursor = conn.cursor() #permet de créer des requêtes SQLite
    print(conn)
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';") #requête SQL permettant de checkez si la base possède déjà des tables
    if cursor.fetchall() == [] : #la fonction .fetchall permet de lister toutes les tables de la db sous forme d'une liste. S'il n'y a pas de tables, c'est que la base est vide
        cursor.execute("CREATE TABLE IF NOT EXISTS User (id INTEGER PRIMARY KEY, name VARCHAR(45), password VARCHAR(45), email VARCHAR(45))")
        cursor.execute("CREATE TABLE IF NOT EXISTS Note (id INTEGER PRIMARY KEY, data VARCHAR(45), date DATETIME, user_id INTEGER NOT NULL, FOREIGN KEY (user_id) REFERENCES User(id))")
        cursor.execute("CREATE TABLE IF NOT EXISTS Classement(id INTEGER PRIMARY KEY, numcas VARCHAR(45), nomsa VARCHAR(45), classref VARCHAR(45), classdate DATETIME, classcatdanger VARCHAR(45), classcodeh VARCHAR(45), classmentiondanger VARCHAR(45), facteurmvaleur VARCHAR(45), facteurmorigine VARCHAR(45), facteurmdate DATETIME)") 
        cursor.execute("CREATE TABLE IF NOT EXISTS Ecotoxicite(id INTEGER PRIMARY KEY, numcas VARCHAR(45), nomsa VARCHAR(45), valpnec VARCHAR(45), unite VARCHAR(45), etudes VARCHAR(45), donneetoxicite VARCHAR(45), valtox VARCHAR(45), unittox VARCHAR(45), facteursecur INTEGER)")
        cursor.execute("CREATE TABLE IF NOT EXISTS Proprietespc(id INTEGER PRIMARY KEY, numcas VARCHAR(45), nomsa VARCHAR(45), propriete VARCHAR(45), valeur VARCHAR(45), unite VARCHAR(45), temperature INTEGER, PH FLOAT, observation VARCHAR(45))")

        filltable("Classement",conn)
        filltable("Ecotoxicite",conn)
        filltable("Proprietespc",conn)
conn.commit() #commit les modifications
conn.close() #ferme la base de données
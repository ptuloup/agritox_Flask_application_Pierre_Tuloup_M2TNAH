import csv, sqlite3, os
from os import path

#tout d'abord, je crée le fichier où doit se trouver la database en vérifiant notamment si elle n'existe déjà pas
if not path.exists("./database/"):
    os.mkdir("./database/")

# l'objectif du programme est de créer une base de données appelées "agritox.db" dans le fichier "database". Ensuite, je regarde si la base existe deja ou pas. Si elle existe, ca passe. Si elle n'existe pas, elle va en créer une à partir des fichiers csv déposés dans le dossier "csvfile"
with sqlite3.connect("./database/agritox.db") as conn: #je crée une variable "conn" qui est la connexion de ma base SQLite. A noter que la fonction connect crée automatiquement la base si elle n'existe pas
    cursor = conn.cursor() #permet de créer des requêtes SQLite
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';") #requête SQL permettant de checkez si la base possède déjà des tables
    if cursor.fetchall() == [] : #la fonction .fetchall permet de lister toutes les tables de la db sous forme d'une liste. S'il n'y a pas de tables, c'est que la base est vide
        files = os.listdir("./csvfile/") #initie une variable comme chemin de fichiers pour boucler dessus
        for file in files:
            arborescence = "./csvfile/" #une variable permettant de reconstruire l'arborescence pour boucler sur les fichiers csv
            if file.endswith(".csv"): #ajoute une sécurité pour récupérer uniquement les fichiers csv
                table = file.replace(".csv", "") #je crée une variable "table" qui est le nom donné à chaque table créée dans la base à partir du nom de chaque fichier csv
                with open(arborescence + file, newline='') as f: #j'ouvre chacun fichier csv
                    reader = csv.reader(f, delimiter = ";")
                    entete = next(reader) #la fonction next permet ici de récupérer la première ligne de chaque fichier csv où se trouvent les en-têtes
                    nombre_colonne = len(entete) #je récupère le nombre de colonnes, cela me servira à initialiser chaque table
                    colonnes = ', '.join(entete) #je transforme la liste des en-têtes en une string que je manipulerai pour l'intégrer dans ma requête SQLite
                    #les 3 prochaines lignes servent à nettoyer la string pour être acceptable dans une requête SQLite
                    colonnes = colonnes.replace("  ", "")
                    colonnes = colonnes.replace(" ,", ",")
                    colonnes = colonnes.replace("/", "_") #le slash cause une erreur en SQL
                    cursor.execute("CREATE TABLE {0} (Cle_primaire INTEGER NOT NULL PRIMARY KEY, {1});".format(table, colonnes)) #requête SQLite permettant de créer la table pour chaque fichier csv, chaque table ayant une colonne de clé primaire + une colonne pour chaque colonne du fichier csv
                    liste_valeur = [] #j'initialise une variable qui sera une liste imbriquée, c'est à dire une liste contenant des listes de toutes les valeurs de chaque ligne
                    n = 1 #je crée un index qui correspond à la clé primaire, inexistante dans les fichiers csv
                    for row in reader : #je boucle sur le csv pour récupérer chaque ligne et les ajoute à ma liste "liste valeur"
                        row = [n] + row #j'ajoute la clé primaire à chaque ligne du csv
                        liste_valeur.append(row) #j'ajoute chaque ligne dans ma variable "liste valeur"
                        n += 1
                    conn.executemany('INSERT INTO {0} VALUES ({1})'.format(table,"?," * (int(nombre_colonne)) + "?"), liste_valeur) #Je mets d'un bloc un fichier csv dans une table, car chaque table correspond à un fichier csv
    else : #ces deux lignes else / pass permettent de ne rien faire si la base existe déjà. Le programme peut donc tourner à chaque itération sans rien consommer.
        pass
conn.commit() #commit les modifications
conn.close() #ferme la base de données
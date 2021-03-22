# Programme servant à transformer un ensemble de fichiers csv en une base de données SQLite #

## Prérequis ##

Créez un environnement virtuel avec la commande virtualenv -p python3 venv

Installez les packages avec pip install -r requirements.txt

## Fonctionnement ##

IMPORTANT : tous les fichiers csv composant la base SQLite doivent être déposés dans un fichier nommé "csvfile" et déposé à la racine.

Le fichier main.py crée (si besoin) le fichier "database" où se trouvera le base de données SQLite.

Ensuite, si la base de données n'existait pas avant, il va :
* prendre tous les fichiers csv situés dans le dossier "csvfile" à la racine. Si vous voulez le faire vous-mêmes, mettez vos propres fichiers dans le dossier "csvfile".
* chaque csv différent créera une table ayant pour titre le nom du fichier csv et ayant pour colonne les colonnes du fichier csv.
* les données de chaque csv seront intégrés et une clé primaire sera ajoutée. C'est un entier non nul croissant.

Le programme peut être lancé en boucle puisqu'un système conditionnel permet de ne pas le lancer si la base de données existait déjà et est déjà remplie.

## Rajout du fichier test.py ##

Le fichier test.py crée la base de données test.db à l'intérieur du dossier website qui contient uniquement une partie des données d'Agritox correspondant à trois tables. Je me suis servi de cette dernière pour la mise en forme de l'application.

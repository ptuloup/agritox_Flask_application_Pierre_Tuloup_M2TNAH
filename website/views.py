from flask import Blueprint, render_template, request, flash, jsonify, url_for, session, redirect
from sqlalchemy import or_
from flask_login import login_required, current_user
from datetime import datetime
from .models import User, Note, Classement, Ecotoxicite, Proprietespc
from . import db
import json

views = Blueprint('views', __name__) # On utilise Blueprint pour pouvoir donner plus facilement accès aux pages.

# Le code qui suit définit les différentes routes de configuration de l'application Flask, reliées aux templates html.
@views.route('/', methods=['GET', 'POST']) # On se place à la racine pour la fonction home page.
@login_required # Pour cela, il faut que l'utilisateur soit connecté. 
def home(): # Définition de la fonction home
    if request.method == 'POST': # Si la méthode correspond à un POST
        note = request.form.get('note') # On crée celle-ci avec un request.form.get

        if len(note) < 1: # Si la longueur du message est strictement inférieure à un caractère
            flash('Note is too short!', category='error') # On renvoie le message d'une note trop courte avec un message d'erreur
        else: # Si la longueur du message est supérieure ou égale à un caractère
            new_note = Note(data=note, user_id=current_user.id) # la nouvelle note est créée
            db.session.add(new_note) # On l'ajoute dans la base de données
            db.session.commit() # On enregistre la base de données
            flash('Note added!', category='success') # On affiche le message flash avec succès

    return render_template("home.html", user=current_user) # Le render template renvoie à la page d'accueil


@views.route('/delete-note', methods=['POST']) # Cette route sert à supprimer un commentaire si besoin
def delete_note(): # Initialisation de la fonction delete_note
    note = json.loads(request.data) # On charge les données en format json
    noteId = note['noteId'] # On appelle l'id utilisateur qui correspond à la note
    note = Note.query.get(noteId)
    if note: # Si la note existe
        if note.user_id == current_user.id: # Si l'utilisateur correspondant est connecté
            db.session.delete(note) # On peut alors supprimer la note de la base de données
            db.session.commit() # On enregistre les modifications.
            flash('Note deleted!', category='success') # On affiche alors le message qui correspond avec succès.

    return jsonify({})


# Pour les routes suivantes, qui correspondent aux tables affichées dans ma base, j'ai procédé par étape et ai fait le choix de garder certaines étapes de construction, notamment certaines lignes print pour les debug ainsi que des parties commentées de code qui m'ont servi pour optimiser l'écriture finale.

@views.route('/classement', methods=['GET', 'POST']) 
def classement():
    DONNEES_PAR_PAGES = 15 
    searchTerm = None

    # En cas de méthode GET, il est possible d'avoir un élément de recherche
    #   On le récupère pour la recherche plus tard.
    if request.method == 'GET':
        searchTerm = request.args.get("searchTerm", type=str)
    
    # Récupération de la page dans les paramètres, avec un défaut de 1 et en integer.
    page = request.args.get("page", 1, int)

    if searchTerm is not None:
        # Si il y a une recherche, on filtre la recherche 
        #   sur l'ensemble des colonnes du tableau Classement 
        #   avec la méthode query.filter ainsi que la méthode 
        #   ilike qui prend en compte chaque colonne.
        classements = Classement.query.filter(
            or_(
                Classement.numcas.ilike("%{}%".format(searchTerm)),
                Classement.classcatdanger.ilike("%{}%".format(searchTerm)),
                Classement.classcodeh.ilike("%{}%".format(searchTerm))
            )
        )
    else:
        # Si ce n'est pas le cas, on laisse affiché l'ensemble des données de la table
        classements = Classement.query

    # La pagination est appliquée sur la query filtrée ou brute, pour éviter
    #    une répétition
    classements = classements.paginate(
        page=page,
        per_page=DONNEES_PAR_PAGES
    )

    # Ci-dessous, on gère les situations où l'utilisateur propose des modifications à la base
    #    de données.
    if request.method == 'POST':
        if current_user.is_authenticated:

            if 'deleteForm' in request.form:
                # On l'utilise pour supprimer les données d'une ligne de la table Classement
                Classement.query.filter(Classement.id == request.form['classement_to_delete']).delete() 
                db.session.commit()
                flash('You deleted data successfully!', category='success')

                return redirect(url_for('.classement')) 

            elif 'editForm' in request.form: 
                # Cette méthode sert à modifier les données de la base et à la mettre à jour
                Classement.query.filter(Classement.id == request.form['classement_to_update']).update({
                    Classement.numcas: request.form['numcas'],
                    Classement.classdate: request.form['classdate'],
                    Classement.classcatdanger: request.form['classcatdanger'],
                    Classement.classcodeh: request.form['classcodeh'],
                    })
                db.session.commit() 
                flash('You edited data successfully!', category='success')

                return redirect(url_for('.classement')) 

            elif 'createForm' in request.form:
                # Cette méthode permet de créer de nouvelles données dans la base de données
                new_classement = Classement(
                    numcas=request.form['numcas'],
                    classdate=request.form['classdate'],
                    classcatdanger=request.form['classcatdanger'],
                    classcodeh=request.form['classcodeh']
                ) 
                db.session.add(new_classement)
                db.session.commit()
                flash('You created new data successfully!', category='success') 

                return redirect(url_for('.classement')) 

            else:
                flash('You must be authenticated', category='error') # Ces fonctionnalités ne sont permises uniquement si l'utilisateur est enregistré.

    return render_template('classement.html', 
        user=current_user, 
        classements=classements,
        searchTerm=searchTerm or ""
    ) 

# Les mêmes étapes que précédemment s'appliquent pour la route de la table Ecotoxicite
@views.route('/ecotoxicite', methods=['GET', 'POST']) # On initialise la route
def ecotoxicite(): # Définition de la fonction pour la route de la table Ecotoxicite
    DONNEES_PAR_PAGES = 15 # On renvoie 15 données par page pour créer une pagination
    searchTerm = None # On crée la fonctionnalité pour chercher à l'intérieur des données de la table
    print(request.method) # Mêmes étapes de debug que précédemment
    if session['searchTerm']: # On utilise l'outil session pour chercher dans la base de données
        print("truc2") # Etapes de debug
        print(session['searchTerm']) # Etapes de debug
        print("truc") # Etapes de debug
        searchTerm = session['searchTerm']
    if request.method == 'POST': # Si la méthode est un POST
        print("test") # Etapes de debug
        print(request.form) # Etapes de debug
        print("test2") # Etapes de debug
        if 'searchForm' in request.form: # Si la méthode du Search existe
            print('search for') # Etapes de debug
            searchTerm = request.form['searchTerm'] # Faire correspondre la recherche dans la base de données
            print(searchTerm) # Etapes de debug
            searchTerm = "%{}%".format(searchTerm) # On applique un formatage au résultat de la recherche.
            session['searchTerm'] = searchTerm 

    page = request.args.get("page", 1) # On affiche les pages correspondant aux résultats de la recherche

    if isinstance(page, str) and page.isdigit(): # Si la recherche donne des résultats, on affiche le numéro des pages correspondant
        page = int(page)
    else:
        page = 1 # Sinon, on affiche uniquement la première page

    ecotoxicites = None # Initialisation de la recherche dans la table Ecotoxicité
    print(searchTerm) # Etapes de debug
    if searchTerm is not None: # Si les mots recherchés existent dans la table Ecotoxicite, on filtre la recherche sur l'ensemble des colonnes de la table Ecotoxicité avec la méthode query.filter ainsi que la méthode ilike qui prend en compte chaque colonne. On garde également la pagination.
        ecotoxicites = Ecotoxicite.query.filter(or_(Ecotoxicite.nomsa.ilike(searchTerm), Ecotoxicite.numcas.ilike(searchTerm), Ecotoxicite.valpnec.ilike(searchTerm), Ecotoxicite.unite.ilike(searchTerm), Ecotoxicite.etudese.ilike(searchTerm))).paginate(
            page=page,
            per_page=DONNEES_PAR_PAGES            
        )
    else: # Si la recherche ne correspond pas, on laisse affiché l'ensemble des données de la table
        ecotoxicites = Ecotoxicite.query.paginate(
            page=page,
            per_page=DONNEES_PAR_PAGES
        )
    print('before') # Etapes de debug
    if request.method == 'POST': # Si la méthode est un POST
        """
        if 'searchForm' in request.form:
            print('search for')
            search_term = request.form['searchTerm']
            print(search_term)
            search_term = "%{}%".format(search_term)
            ecotoxicites = Ecotoxicite.query.filter(Ecotoxicite.numcas.ilike(search_term)).paginate(
                page=page,
                per_page=DONNEES_PAR_PAGES
    )
            print(ecotoxicites.items)"""
        if current_user.is_authenticated: # Si l'utilisateur est connecté
            if 'deleteForm' in request.form: # On cherche à utiliser la fonctionnalité CRUD Delete dans la table
                Ecotoxicite.query.filter(Ecotoxicite.id == request.form['ecotoxicite_to_delete']).delete() # On supprimer les données choisies
                db.session.commit() # On enregistre la modification dans la base de données
                flash('You deleted data successfully!', category='success') # On affiche le message suivant avec succès
                return redirect(url_for('ecotoxicite')) # On renvoie à la page html de la table
            elif 'editForm' in request.form: # Cette méthode permet de mettre à jour et de pouvoir modifier les données
                Ecotoxicite.query.filter(Ecotoxicite.id == request.form['ecotoxicite_to_update']).update({ 
                    Ecotoxicite.nomsa: request.form['nomsa'],
                    Ecotoxicite.numcas: request.form['numcas'],
                    Ecotoxicite.valpnec: request.form['valpnec'],
                    Ecotoxicite.unite: request.form['unite'],
                    Ecotoxicite.etudese: request.form['etudese']
                    }) # On applique les modifications dans la base de données
                db.session.commit() # On enregistre les modification dans la base de données
                flash('You edited data successfully!', category='success') # On affiche le message suivant avec succès

                
            elif 'createForm' in request.form: # Cette méthode permet de créer de nouvelles données dans la base de données. L'utilisateur remplit les champs correspondant au nombre de colonnes de la table, et dans l'ordre de création indiqué.
                new_ecotoxicite = Ecotoxicite(numcas=request.form['numcas'], nomsa=request.form['nomsa'], valpnec=request.form['valpnec'], unite=request.form['unite'], etudese=request.form['etudese'])
                db.session.add(new_ecotoxicite) # On ajoute les modifications dans la base de données
                db.session.commit() # On enregistre
                flash('You created new data successfully!', category='success') # On affiche le message suivant avec succès
        else :
            flash('You must be authenticated', category='error') # Il faut pour cela que l'utilisateur soit connecté

    return render_template('ecotoxicite.html', user=current_user, ecotoxicites=ecotoxicites) # On affiche la page correspondant à la table avec les modifications apportées.

# les mêmes étapes que précédemment s'appliquent pour la route de la table Proprietespc (Propriétés physico-chimiques)
@views.route('/proprietespc', methods=['GET', 'POST']) # On initialise la route de la table Proprietespc
def proprietespc(): # Définition de la fonction proprietespc
    DONNEES_PAR_PAGES = 15 # On affiche 15 résultats par page
    searchTerm = None # On initialise la fonctionnalité pour chercher dans la base.
    print(request.method) # Etapes de debug
    if session['searchTerm']: # On utilise l'outil session pour chercher dans la base
        print("truc2") # Etapes de debug
        print(session['searchTerm']) # Etapes de debug
        print("truc") # Etapes de debug
        searchTerm = session['searchTerm'] # On renvoie les termes de la recherche dans la base de données
    if request.method == 'POST': # Si la méthode est un POST
        print("test") # Etapes de debug
        print(request.form) # Etapes de debug
        print("test2") # Etapes de debug
        if 'searchForm' in request.form: # Si la méthode searchForm existe
            print('search for') # Etapes de debug
            searchTerm = request.form['searchTerm'] # On l'applique à notre recherche
            print(searchTerm) # Etapes de debug
            searchTerm = "%{}%".format(searchTerm) # On applique un formatage aux résultats de la recherche
            session['searchTerm'] = searchTerm # On l'applique à la base de données

    page = request.args.get("page", 1) # On affiche les pages correspondant aux résultats de la recherche

    if isinstance(page, str) and page.isdigit(): # Si la recherche donne des résultats, on affiche les pages avec le numéro à chaque page qui correspond à la recherche.
        page = int(page) # Le numéro de page est un entier
    else:
        page = 1 # Sinon, on affiche toutes les données de la table si la recherche est infructueuse.

    proprietespcs = None # Initialisation de la recherche dans la table Proprietespc
    print(searchTerm) # Etapes de debug (terminal)
    if searchTerm is not None: # Si les mots recherchés existent dans la table Proprietespc, on filtre la recherche sur l'ensemble des colonnes de la table Proprietespc avec la méthode query.filter et le or_ de sqlalchemy ainsi que la méthode ilike qui prend en compte chaque colonne. On garde également la pagination.
        proprietespcs = Proprietespc.query.filter(or_(Proprietespc.numcas.ilike(searchTerm), Proprietespc.valeur.ilike(searchTerm), Proprietespc.propriete.ilike(searchTerm), Proprietespc.unite.ilike(searchTerm), Proprietespc.temperatures.ilike(searchTerm))).paginate(
            page=page,
            per_page=DONNEES_PAR_PAGES            
        )
    else: # Si la recherche ne correspond pas aux données, on affiche l'ensemble des données. La recherche d'un champ vide affiche normalement l'ensemble des données de la table.
        proprietespcs = Proprietespc.query.paginate(
            page=page,
            per_page=DONNEES_PAR_PAGES
        )
    print('before') # Etapes de debug

    if request.method == 'POST': # Si la méthode est un POST
        """
        if 'searchForm' in request.form:
            print('search for')
            search_term = request.form['searchTerm']
            print(search_term)
            search_term = "%{}%".format(search_term)
            proprietespcs = Proprietespc.query.filter(Proprietespc.numcas.ilike(search_term)).paginate(
                page=page,
                per_page=DONNEES_PAR_PAGES
    )
            print(proprietespcs.items)"""
        if current_user.is_authenticated: # Si l'utilisateur est connecté
            if 'deleteForm' in request.form: # Cette méthode permet de supprimer les données de la base de données
                Proprietespc.query.filter(Proprietespc.id == request.form['proprietespc_to_delete']).delete() # On applique le Delete du CRUD dans la base de données
                db.session.commit() # On enregistre les modification dans la base de données
                flash('You deleted data successfully!', category='success') # On affiche le message suivant avec succès
                return redirect(url_for('proprietespc')) # On renvoie à la page html Proprietespc
            elif 'editForm' in request.form: # Cette méthode permet de mettre à jour et modifier les données de la base de données
                Proprietespc.query.filter(Proprietespc.id == request.form['proprietespc_to_update']).update({
                    Proprietespc.numcas: request.form['numcas'],
                    Proprietespc.valeur: request.form['valeur'],
                    Proprietespc.propriete: request.form['propriete'],
                    Proprietespc.unite: request.form['unite'],
                    Proprietespc.temperatures: request.form['temperatures']
                    }) # On applique cette méthode sur chaque champ
                db.session.commit() # On enregistre
                flash('You edited data successfully!', category='success') # On affiche le message suivant avec succès

                
            elif 'createForm' in request.form: # Cette méthode permet de créer de nouvelles données dans la base de données, dans l'ordre indiqué.
                new_proprietespc = Proprietespc(numcas=request.form['numcas'], valeur=request.form['valeur'], propriete=request.form['propriete'], unite=request.form['unite'], temperatures=request.form['temperatures'])
                db.session.add(new_proprietespc) 
                db.session.commit() # On enregistre
                flash('You created new data successfully!', category='success') # On affiche le message suivant avec succès
        else :
            flash('You must be authenticated', category='error') # Il faut que l'utilisateur soit connecté pour utiliser ces fonctionnalités.

    return render_template('proprietespc.html', user=current_user, proprietespcs=proprietespcs) # On renvoie à la page html Proprietespc avec les modifications effectuées.


@views.route('/notes', methods=['GET', 'POST']) # On initialise la route de la table Notes
def note(): # Définition de la fonction qui permet d'ajouter des commentaires
    notes = Note.query[:]
    if request.method == 'POST':
        now = datetime.now() # On enregistre les données avec l'heure d'ajout.
        new_notes = Note(data=request.form['data'], date=now, user_id=current_user.id)
        db.session.add(new_notes) 
        db.session.commit() # On enregistre dans la base de données
        flash('You just created new notes successfully!', category='success') # On affiche le message suivant avec succès

    return render_template('notes.html', user=current_user, notes=notes) # On renvoie à la page html Notes.

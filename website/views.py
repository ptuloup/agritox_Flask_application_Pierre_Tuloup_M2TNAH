from flask import Blueprint, render_template, request, flash, jsonify, url_for
from flask_login import login_required, current_user
from datetime import datetime
from .models import User, Note, Classement, Ecotoxicite, Proprietespc
from . import db
import json

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        note = request.form.get('note')

        if len(note) < 1:
            flash('Note is too short!', category='error')
        else:
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note added!', category='success')

    return render_template("home.html", user=current_user)


@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()
            flash('Note deleted!', category='success')

    return jsonify({})

@views.route('/classement', methods=['GET', 'POST'])
def classement():
    DONNEES_PAR_PAGES = 15

    page = request.args.get("page", 1)

    if isinstance(page, str) and page.isdigit():
        page = int(page)
    else:
        page = 1

    classements = Classement.query.paginate(
        page=page,
        per_page=DONNEES_PAR_PAGES
    )
    print('before')
    if request.method == 'POST':
        print('post')
        if 'searchForm' in request.form:
            print('search for')
            search_term = request.form['searchTerm']
            print(search_term)
            search_term = "%{}%".format(search_term)
            classements = Classement.query.filter(Classement.numcas.ilike(search_term)).paginate(
                page=page,
                per_page=DONNEES_PAR_PAGES
    )
            print(classements.items)

        elif 'deleteForm' in request.form:
            Classement.query.filter(Classement.id == request.form['classement_to_delete']).delete()
            db.session.commit()
            flash('You deleted data successfully!', category='success')
            return redirect(url_for('classement'))
        elif 'editForm' in request.form:
            Classement.query.filter(Classement.id == request.form['classement_to_update']).update({
                Classement.numcas: request.form['numcas'],
                Classement.classdate: request.form['classdate'],
                Classement.classcatdanger: request.form['classcatdanger'],
                Classement.classcodeh: request.form['classcodeh'],
                })
            db.session.commit()
            flash('You edited data successfully!', category='success')

            
        elif 'createForm' in request.form:
            new_classement = Classement(numcas=request.form['numcas'], classdate=request.form['classdate'], classcatdanger=request.form['classcatdanger'], classcodeh=request.form['classcodeh'])
            db.session.add(new_classement) 
            db.session.commit()
            flash('You created new data successfully!', category='success')
        

    return render_template('classement.html', user=current_user, classements=classements)

@views.route('/ecotoxicite', methods=['GET', 'POST'])
def ecotoxicite():
    DONNEES_PAR_PAGES = 15

    page = request.args.get("page", 1)

    if isinstance(page, str) and page.isdigit():
        page = int(page)
    else:
        page = 1

    ecotoxicites = Ecotoxicite.query.paginate(
        page=page,
        per_page=DONNEES_PAR_PAGES
    )
    if request.method == 'POST':
        if 'searchForm' in request.form:
            print('search for')
            search_term = request.form['searchTerm']
            print(search_term)
            search_term = "%{}%".format(search_term)
            ecotoxicites = Ecotoxicite.query.filter(Ecotoxicite.numcas.ilike(search_term)).paginate(
                page=page,
                per_page=DONNEES_PAR_PAGES
    )
            print(ecotoxicites.items)
        if 'deleteForm' in request.form:
            Ecotoxicite.query.filter(Ecotoxicite.id == request.form['ecotoxicite_to_delete']).delete()
            db.session.commit()
            flash('You deleted data successfully!', category='success')
            return redirect(url_for('ecotoxicite'))
        elif 'editForm' in request.form:
            Ecotoxicite.query.filter(Ecotoxicite.id == request.form['ecotoxicite_to_update']).update({
                Ecotoxicite.nomsa: request.form['nomsa'],
                Ecotoxicite.numcas: request.form['numcas'],
                Ecotoxicite.valpnec: request.form['valpnec'],
                Ecotoxicite.unite: request.form['unite'],
                Ecotoxicite.etudese: request.form['etudese']
                })
            db.session.commit()
            flash('You edited data successfully!', category='success')

            
        elif 'createForm' in request.form:
            new_ecotoxicite = Ecotoxicite(numcas=request.form['numcas'], nomsa=request.form['nomsa'], valpnec=request.form['valpnec'], unite=request.form['unite'], etudese=request.form['etudese'])
            db.session.add(new_ecotoxicite) 
            db.session.commit()
            flash('You created new data successfully!', category='success')

    return render_template('ecotoxicite.html', user=current_user, ecotoxicites=ecotoxicites)

@views.route('/proprietespc', methods=['GET', 'POST'])
def proprietespc():
    DONNEES_PAR_PAGES = 15

    page = request.args.get("page", 1)

    if isinstance(page, str) and page.isdigit():
        page = int(page)
    else:
        page = 1

    proprietespcs = Proprietespc.query.paginate(
        page=page,
        per_page=DONNEES_PAR_PAGES
    )
    if request.method == 'POST':
        if 'searchForm' in request.form:
            print('search for')
            search_term = request.form['searchTerm']
            print(search_term)
            search_term = "%{}%".format(search_term)
            proprietespcs = Proprietespc.query.filter(Proprietespc.numcas.ilike(search_term)).paginate(
                page=page,
                per_page=DONNEES_PAR_PAGES
    )
            print(proprietespcs.items)
        if 'deleteForm' in request.form:
            Proprietespc.query.filter(Proprietespc.id == request.form['proprietespc_to_delete']).delete()
            db.session.commit()
            flash('You deleted data successfully!', category='success')
            return redirect(url_for('proprietespc'))
        elif 'editForm' in request.form:
            Proprietespc.query.filter(Proprietespc.id == request.form['proprietespc_to_update']).update({
                Proprietespc.numcas: request.form['numcas'],
                Proprietespc.valeur: request.form['valeur'],
                Proprietespc.propriete: request.form['propriete'],
                Proprietespc.unite: request.form['unite'],
                Proprietespc.temperatures: request.form['temperatures']
                })
            db.session.commit()
            flash('You edited data successfully!', category='success')

            
        elif 'createForm' in request.form:
            new_proprietespc = Proprietespc(numcas=request.form['numcas'], valeur=request.form['valeur'], propriete=request.form['propriete'], unite=request.form['unite'], temperatures=request.form['temperatures'])
            db.session.add(new_proprietespc) 
            db.session.commit()
            flash('You created new data successfully!', category='success')

    return render_template('proprietespc.html', user=current_user, proprietespcs=proprietespcs)


@views.route('/notes', methods=['GET', 'POST'])
def note():
    notes = Note.query[:]
    if request.method == 'POST':
        now = datetime.now()
        new_notes = Note(data=request.form['data'], date=now, user_id=current_user.id)
        db.session.add(new_notes) 
        db.session.commit()
        flash('You just created new notes successfully!', category='success')

    return render_template('notes.html', user=current_user, notes=notes)
from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user


auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST']) # Lorsque Flask reçoit une demande pour login, il appelle la fonction login de views et utilise la valeur de retour comme réponse.
def login():
    if request.method == 'POST': # Si l'utilisateur a soumis le formulaire, la request.method sera POST. Dans ce cas, on commence à valider la suite.
        email = request.form.get('email') # Récupération de l'email 
        password = request.form.get('password') # Récupération du password

        user = User.query.filter_by(email=email).first() # On filtre les utilisateurs par leur email et on affiche le premier résultat.
        if user:
            if check_password_hash(user.password, password): # On crypte le mot de passe avec du hash pour plus de sécurité.
                flash('Logged in successfully!', category='success') # Une fois l'utilisateur connecté, on affiche le message 'Logged in sucessfully' et on définit une catégorie pour ne pas avoir d'erreurs.
                login_user(user, remember=True) # On stocke les informations de connexion du user dans la base.
                return redirect(url_for('views.home')) # Une fois l'utilisateur connecté, la page 'home.html' s'affiche.
            else:
                flash('Incorrect password, try again.', category='error') # Si l'utilisateur ne parvient pas à se connecter, il doit réessayer un nouveau mot de passe.
        else:
            flash('Email does not exist.', category='error') # Si l'utilisateur se connecte avec un mauvais mot de passe, ce message s'affiche.

    return render_template("login.html", user=current_user) # Une fois l'utilisateur connecté, les autres templates s'affichent.


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        name = request.form.get('name')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists.', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif len(name) < 2:
            flash('First name must be greater than 1 character.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else:
            new_user = User(email=email, name=name, password=generate_password_hash(
                password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account created!', category='success')
            return redirect(url_for('views.home'))

    return render_template("sign_up.html", user=current_user)

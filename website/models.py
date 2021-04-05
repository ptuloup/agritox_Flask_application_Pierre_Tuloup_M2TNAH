from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

# On configure les tables SQL présentes dans la base de données pour pouvoir ensuite les traiter.

class Note(db.Model):
    __tablename__ = 'Note'
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'))


class User(db.Model, UserMixin):
    __tablename__ ='User'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    name = db.Column(db.String(150))
    notes = db.relationship('Note')

class Classement(db.Model):
    __tablename__ = 'classement'
    id = db.Column(db.Integer, primary_key=True)
    numcas = db.Column(db.String(150))
    nomsa = db.Column(db.String(150))
    classref = db.Column(db.String(150))
    classdate = db.Column(db.String(30)) #change to datetime ?
    classcatdanger = db.Column(db.String(150))
    classcodeh = db.Column(db.String(150))
    classmentiondanger = db.Column(db.String(150))
    facteurmvaleur = db.Column(db.String(150))
    facteurmorigine = db.Column(db.String(150))
    facteurmdate = db.Column(db.String(30)) # change to datetime?

class Ecotoxicite(db.Model):
    __tablename__ = 'ecotoxicite'
    id = db.Column(db.Integer, primary_key=True)
    numcas = db.Column(db.String(150))
    nomsa = db.Column(db.String(150))
    valpnec = db.Column(db.Float)
    unite = db.Column(db.String(150))
    etudese = db.Column(db.String(150))
    donneestoxicite = db.Column(db.String(150))
    valtox = db.Column(db.Float)
    unittox = db.Column(db.String(150))
    facteursecur = db.Column(db.Integer)


class Proprietespc(db.Model):
    __tablename__ = 'proprietespc'
    id = db.Column(db.Integer, primary_key=True)
    numcas = db.Column(db.String(150))
    nomsa = db.Column(db.String(150))
    propriete = db.Column(db.String(150))
    valeur = db.Column(db.String(150))
    unite = db.Column(db.String(150))
    temperatures = db.Column(db.String(150))
    PH = db.Column(db.String(150))
    observation = db.Column(db.String(150))


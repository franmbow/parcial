from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

class Datos(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(60), nullable=False)
    ciudad = db.Column(db.String(60), nullable=False)
    edad = db.Column(db.Integer)
    email = db.Column(db.String(40), unique=True, nullable=False)
    # TODO: agregar al menos 4 atributos más (texto, numérico, etc.)

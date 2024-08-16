from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Schema(db.Model):
    __tablename__ = 'schemas'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    database = db.Column(db.String(50))
    schema = db.Column(db.String(50))
    mode = db.Column(db.String(50))
    delete_days = db.Column(db.Integer(), nullable=True)

class Directory(db.Model):
    __tablename__ = 'directories'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    path = db.Column(db.String(50)) #путь
    mode = db.Column(db.String(50))
    delete_days = db.Column(db.Integer(), nullable=True)
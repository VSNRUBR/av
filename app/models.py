from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Citizen(db.Model):
    _id = db.Column('id', db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    car = db.Column(db.String(15), default='Possible')

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f'Citizen {self.name} was registered.'

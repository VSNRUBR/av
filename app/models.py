from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Citizen(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    sale_opportunity = db.Column(db.Boolean, unique=False, default=True)
    cars = db.relationship('Car', backref='citizen', lazy='dynamic')

    def __init__(self, name, sale_op):
        self.name = name
        self.sale_opportunity = sale_op

    def __repr__(self):
        return f'Citizen {self.name} was registered.'


class Car(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    color = db.Column(db.String(6), nullable=False)
    model = db.Column(db.String(11), nullable=False)
    citizen_id = db.Column(db.Integer, db.ForeignKey('citizen.id'), nullable=False)

    def __repr__(self):
        return f'Car {self.id} was registered.'

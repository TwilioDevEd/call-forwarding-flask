from call_forward_flask import db


class State(db.Model):
    """id | name | senators"""
    __tablename__ = 'states'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    senators = db.relationship('Senator', backref='state', lazy='dynamic')

    def __init__(self, name):
        self.name = name


class Zip(db.Model):
    """id | zip | state (fk)"""
    __tablename__ = 'zipcodes'

    id = db.Column(db.Integer, primary_key=True)
    zipcode = db.Column(db.String, nullable=False)
    state_id = db.Column(db.Integer, db.ForeignKey('states.id'))

    def __init__(self, zipcode, state):
        self.zipcode = zipcode
        self.state = state

class Senator(db.Model):
    """id | state (fk) | name | phone"""
    __tablename__ = 'senators'

    id = db.Column(db.Integer, primary_key=True)
    state_id = db.Column(db.Integer, db.ForeignKey('states.id'))
    name = db.Column(db.String, nullable=False)
    phone = db.Column(db.String, nullable=False)

    def __init__(self, name, phone_number):
        self.name = name
        self.phone = phone_number

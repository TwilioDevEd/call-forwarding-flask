from app import db

class StateSenator(db.Model):
    """id | state | name | phone"""
    __tablename__ = 'state_senators'

    id = db.Column(db.Integer, primary_key=True)
    state = db.Column(db.String, nullable=False)
    name = db.Column(db.String, nullable=False)
    phone_number = db.Column(db.String, nullable=False)

    def __init__(self, state, name, phone_number):
        self.state = state
        self.name = name
        self.phone = phone_number


class Zip(db.Model):
    """id | zip | state"""
    __tablename__ = 'zip_codes'

    id = db.Column(db.Integer, primary_key=True)
    zipcode = db.Column(db.String, nullable=False)
    state = db.Column(db.String, nullable=False)

    def __init__(self, zipcode, state):
        self.zipcode = zipcode
        self.state = state

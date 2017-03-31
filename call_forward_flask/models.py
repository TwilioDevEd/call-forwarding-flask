from call_forward_flask import db


class State(db.Model):
    """Schema for State model."""

    __tablename__ = 'states'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    senators = db.relationship('Senator', backref='state', lazy='dynamic')

    def __init__(self, name):
        self.name = name


class Zipcode(db.Model):
    """Schema for Zipcode model."""

    __tablename__ = 'zipcodes'

    id = db.Column(db.Integer, primary_key=True)
    zipcode = db.Column(db.String, nullable=False)
    state = db.Column(db.String, nullable=False)

    def __init__(self, zipcode, state):
        self.zipcode = zipcode
        self.state = state

    @property
    def state_id(self):
        """Get State ID from zipcode."""
        state_obj = State.query.filter_by(name=self.state).first()
        return state_obj.id


class Senator(db.Model):
    """Schema for Senator model."""

    __tablename__ = 'senators'

    id = db.Column(db.Integer, primary_key=True)
    state_id = db.Column(db.Integer, db.ForeignKey('states.id'))
    name = db.Column(db.String, nullable=False)
    phone = db.Column(db.String, nullable=False)

    def __init__(self, name, phone_number):
        self.name = name
        self.phone = phone_number

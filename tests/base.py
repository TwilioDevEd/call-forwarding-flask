"""Test base for call_forward_flask tests."""
from unittest import TestCase

from call_forward_flask import app, db
from call_forward_flask.models import Senator, State, Zipcode


class BaseTest(TestCase):
    """Test base case. Includes setup, teardown, and db setup/teardown."""

    def setUp(self):
        self.client = app.test_client()
        db.create_all()
        self.seed()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def seed(self):
        """Seed test db with small dataset for testing."""
        self.senator1 = Senator(name='Kat Kent', phone_number='+12174412652 ')
        db.session.add(self.senator1)
        self.senator2 = Senator(name='Foo Bar', phone_number='+19523334441 ')
        db.session.add(self.senator2)

        self.state = State(name='IL')
        self.state.senators = [self.senator1, self.senator2]
        db.session.add(self.state)

        self.test_zip = Zipcode(zipcode='60616', state='IL')
        db.session.add(self.test_zip)
        db.session.commit()

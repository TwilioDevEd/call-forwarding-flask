from call_forward_flask.models import (
    Senator,
    State,
    Zipcode,
)

from xmlunittest import XmlTestCase


class BaseTest(XmlTestCase):

    def setUp(self):
        from call_forward_flask import app, db
        self.app = app
        self.app.config['WTF_CSRF_ENABLED'] = False
        self.db = db
        self.client = self.app.test_client()
        self.seed()

    def tearDown(self):
        self.delete_senators()
        self.delete_states()
        self.db.session.commit()

    def delete_states(self):
        State.query.delete()

    def delete_senators(self):
        Senator.query.delete()

    def seed(self):
        """Seed test db with small dataset for testing."""
        self.senator1 = Senator(
            name='Kat Kent',
            phone_number='+16468635472'
        )
        self.db.save(self.senator1)
        self.senator2 = Senator(
            name='Foo Bar',
            phone_number='+17738095281'
        )
        self.db.save(self.senator2)

        self.state = State(name='IL')
        self.state.senators = ([self.senator1, self.senator2])
        self.db.save(self.state)

        self.test_zip = Zipcode(zipcode='60616', state='IL')
        self.db.save(self.test_zip)

"""View tests for call_forward_flask application."""
from xml.etree import ElementTree

from .base import BaseTest

from flask import url_for


class CallForwardTests(BaseTest):
    """Tests for our call_forward_flask views."""

    def test_root_route(self):
        """Test that our / route uses the index.html landing page."""
        response = self.client.get('/')

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Call Forward", response.data)

    def test_get_state_on_call_no_from_state_triggers_lookup(self):
        """Test that an incoming call missing state data collects zipcode."""
        response = self.client.post('/callcongress/welcome')
        root = ElementTree.fromstring(response.data)

        # Assert that we Gather data from caller
        self.assertEqual(len(root.findall('./Gather')), 1)

        # Assert that caller is redirected to state_lookup
        self.assertEqual(
            root.find('./Gather').get('action'), '/callcongress/state-lookup'
        )

    def test_get_state_on_call_with_from_state(self):
        """Test that an incoming call with fromState will set state."""
        response = self.client.post('/callcongress/welcome', data=dict(FromState='IL'))
        root = ElementTree.fromstring(response.data)

        # Assert that we gather data from the caller
        self.assertEqual(len(root.findall('./Gather')), 1)

        # Assert that the caller is redirected to set_state
        self.assertEqual(root.find('./Gather').get('action'), '/callcongress/set-state')

        # Assert redirect contains caller's from_state
        self.assertEqual(root.find('./Gather').get('fromState'), 'IL')

    def test_post_to_set_state_with_digit_1(self):
        """User who accepts state should be directed to senator call."""
        response = self.client.post(
            '/callcongress/set-state',
            data=dict(Digits='1', CallerState='IL'),
            follow_redirects=True,
        )
        root = ElementTree.fromstring(response.data)

        # Assert that we don't try to Gather any more data
        self.assertIsNone(root.find('./Gather'))

        # Assert Dial to 1st senator
        self.assertEqual(root.find('./Dial').text, self.senator1.phone)

    def test_post_to_set_state_with_digit_2(self):
        """User who doesn't accept state should be asked for zipcode."""
        response = self.client.post(
            '/callcongress/set-state', data=dict(Digits="2"), follow_redirects=True
        )
        root = ElementTree.fromstring(response.data)

        # Assert that we gather 5 digits for zipcode
        self.assertEqual(len(root.findall('./Gather')), 1)
        self.assertEqual(root.find('./Gather').get('numDigits'), '5')

        # Assert keypress directs to state_lookup
        self.assertEqual(
            root.find('./Gather').get('action'), '/callcongress/state-lookup'
        )

    def test_state_lookup_by_zip(self):
        """Test that we can get a state from a given zipcode."""
        response = self.client.post(
            '/callcongress/state-lookup', data=dict(Digits="60616"), follow_redirects=True
        )

        root = ElementTree.fromstring(response.data)

        self.assertEqual(
            root.find('./Say').text,
            f"Connecting you to {self.senator1.name}. "
            "After the senator's office ends the call, you "
            f"will be re-directed to {self.senator2.name}."
        )

        # Assert that we've followed the redirect and will send to second
        self.assertEqual(
            root.find('./Dial').get('action'),
            f'/callcongress/call-second-senator/{self.senator2.id}',
        )

    def test_call_senators_dials_first_sen(self):
        """Test an incoming call from IL routes to 1st IL senator."""
        response = self.client.post(url_for('call_senators', state_id=1))
        root = ElementTree.fromstring(response.data)

        self.assertEqual(self.senator1.phone, root.find('./Dial').text)

    def test_call_senators_redirects_to_second(self):
        """Test that this route will redirect to second sen after call ends."""
        response = self.client.post(url_for('call_senators', state_id=1))
        root = ElementTree.fromstring(response.data)

        self.assertEqual(
            f'/callcongress/call-second-senator/{self.senator2.id}',
            root.find('./Dial').get('action'),
        )

    def test_call_second_senator(self):
        """Test call_second_senator dials second senator."""
        response = self.client.post(
            url_for('call_second_senator', senator_id=self.senator2.id)
        )
        root = ElementTree.fromstring(response.data)

        self.assertEqual(self.senator2.phone, root.find('./Dial').text)

    def test_call_second_senator_redirects_to_goodbye(self):
        """Test that this route will redirect to /goodbye after call ends."""
        response = self.client.post(
            url_for('call_second_senator', senator_id=self.senator1.id)
        )
        root = ElementTree.fromstring(response.data)

        self.assertEqual('/callcongress/goodbye', root.find('./Dial').get('action'))

    def test_goodbye_hangs_up(self):
        """Test end_call route for messaging and hangup."""
        response = self.client.post(url_for('end_call'))
        root = ElementTree.fromstring(response.data)

        self.assertEqual(
            "Thank you for using Call Congress! Your voice makes a difference. Goodbye.",
            root.find('./Say').text,
        )
        self.assertEqual(len(root.findall('./Hangup')), 1)

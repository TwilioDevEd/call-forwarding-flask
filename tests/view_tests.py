from base import BaseTest

from call_forward_flask.models import(
    State,
)

from flask import url_for


class CallForwardTests(BaseTest):

    def test_root_route(self):
        """Test that our / route uses the index.html landing page."""
        response = self.client.get('/')

        self.assertEqual(response.status_code, 200)
        self.assertTrue("Call Forward" in response.data)

    def test_get_state_on_call_no_from_state_triggers_lookup(self):
        """Test that an incoming call missing state data collects zipcode."""
        response = self.client.post('/callcongress/welcome')
        root = self.assertXmlDocument(response.data)

        # Assert that we Gather data from caller
        self.assertEqual(len(root.xpath('./Gather')), 1)

        # Assert that caller is redirected to state_lookup
        self.assertEqual(
            root.xpath('./Gather')[0].get('action'),
            '/callcongress/state-lookup'
        )

    def test_get_state_on_call_with_from_state(self):
        response = self.client.post(
            '/callcongress/welcome', data=dict(FromState='IL')
        )
        root = self.assertXmlDocument(response.data)

        # Assert that we gather data from the caller
        self.assertEqual(len(root.xpath('./Gather')), 1)

        # Assert that the caller is redirected to set_state
        self.assertEqual(
            root.xpath('./Gather')[0].get('action'),
            '/callcongress/set-state'
        )

        # Assert redirect contains caller's from_state
        self.assertEqual(
            root.xpath('./Gather')[0].get('from_state'),
            'IL'
        )

    def test_post_to_set_state_with_digit_1(self):
        """User who accepts state should be directed to senator call."""

        caller_state = 'IL'
        response = self.client.post(
            '/callcongress/set-state',
            data=dict(Digits='1', CallerState=caller_state),
            follow_redirects=True
        )
        root = self.assertXmlDocument(response.data)

        il = State.query.filter_by(name=caller_state).first()
        # Get the 'second' senator for this state
        sen_phone = il.senators.first().phone

        # Assert that we don't try to Gather any more data
        self.assertEqual(len(root.xpath('./Gather')), 0)

        # Assert Dial to 1st senator
        self.assertEqual(root.xpath('./Dial')[0].text, sen_phone)

    def test_post_to_set_state_with_digit_2(self):
        """User who doesn't accept state should be asked for zipcode."""
        response = self.client.post(
            '/callcongress/set-state',
            data=dict(Digits="2"),
            follow_redirects=True
        )
        root = self.assertXmlDocument(response.data)

        # Assert that we gather 5 digits for zipcode
        self.assertEqual(len(root.xpath('./Gather')), 1)
        self.assertEqual(root.xpath('./Gather')[0].get('numDigits'), '5')

        # Assert keypress directs to state_lookup
        self.assertEqual(
            root.xpath('./Gather')[0].get('action'),
            '/callcongress/state-lookup'
        )

    def test_state_lookup_by_zip(self):
        """Test that we can get a state from a given zipcode."""
        response = self.client.post(
            '/callcongress/state-lookup',
            data=dict(Digits="60616"),
            follow_redirects=True
        )

        root = self.assertXmlDocument(response.data)

        # IL state id (maps to zipcode 60616)
        state_id = State.query.filter_by(name='IL').first().id

        # Assert we tell the caller we're connecting them
        senators = State.query.get(state_id).senators.all()
        first_sen = senators[0]
        second_sen = senators[1]
        forwarding_str = (
            "Connecting you to {}. ".format(first_sen.name) +
            "After the senator's office ends the call, you " +
            "will be re-directed to {}.".format(second_sen.name)
        )
        self.assertEqual(
            root.xpath('./Say')[0].text,
            forwarding_str
        )

        # Assert that we've followed the redirect and will send to second
        self.assertEqual(
            root.xpath('./Dial')[0].get('action'),
            '/callcongress/call-second-senator/{}'.format(second_sen.id)
        )

    def test_call_senators_dials_first_sen(self):
        """Test an incoming call from IL routes to 1st IL senator."""
        response = self.client.post(url_for('call_senators', state_id=1))
        root = self.assertXmlDocument(response.data)

        il = State.query.filter_by(name='IL').first()
        il_sen_phone = il.senators.first().phone

        self.assertEqual(
            [il_sen_phone],
            root.xpath('./Dial/text()')
        )

    def test_call_senators_redirects_to_second(self):
        """Test that this route will redirect to second sen after call ends."""
        state_id = 1
        senators = State.query.get(state_id).senators.all()

        response = self.client.post(
            url_for('call_senators', state_id=state_id)
        )
        root = self.assertXmlDocument(response.data)
        next_sen_route = '/callcongress/call-second-senator/{}'.format(
            senators[1].id
        )
        self.assertEqual(
            next_sen_route,
            root.xpath('./Dial')[0].get('action')
        )

    def test_call_second_senator(self):
        """Test call_second_senator dials second senator."""
        il = State.query.filter_by(name='IL').first()
        senators = State.query.get(il.id).senators.all()

        response = self.client.post(url_for(
            'call_second_senator', senator_id=senators[1].id)
        )
        root = self.assertXmlDocument(response.data)

        self.assertEqual(
            [senators[1].phone],
            root.xpath('./Dial/text()')
        )

    def test_call_second_senator_redirects_to_goodbye(self):
        """Test that this route will redirect to /goodbye after call ends."""
        il = State.query.filter_by(name='IL').first()
        senators = State.query.get(il.id).senators.all()

        response = self.client.post(url_for(
            'call_second_senator', senator_id=senators[1].id)
        )
        root = self.assertXmlDocument(response.data)
        goodbye_route = '/callcongress/goodbye'
        self.assertEqual(
            goodbye_route,
            root.xpath('./Dial')[0].get('action')
        )

    def test_goodbye_hangs_up(self):
        """Test end_call route for messaging and hangup."""
        response = self.client.post(url_for('end_call'))
        root = self.assertXmlDocument(response.data)
        goodbye_msg = ("Thank you for using Call Congress! " +
                       "Your voice makes a difference. Goodbye.")

        self.assertEqual(
            [goodbye_msg],
            root.xpath('./Say/text()')
        )
        self.assertEqual(len(root.xpath('./Hangup')), 1)

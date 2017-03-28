import json

from call_forward_flask import db
from call_forward_flask.models import (
    Senator,
    State,
    Zip,
)


def data_from_json(data):
    state_list = json.loads(data).get('states')

    for s in state_list:
        state = State(name=s)
        state.senators = senators_from_json(json.loads(data).get(s))
        db.save(state)

    return



def senators_from_json(senator_data):
    """Parse senator data from json file for db."""
    senators = []

    for senator in senator_data:
        name = senator['name'],
        state = senator['state'],
        phone = senator['phone']

        senators.append(Senator(name=name[0], phone_number=phone))

    return senators

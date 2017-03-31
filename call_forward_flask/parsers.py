import json

from call_forward_flask import db
from call_forward_flask.models import (
    Senator,
    State,
    Zipcode,
)


def data_from_json(data):
    """Load data and set state/senators on db."""
    state_list = json.loads(data).get('states')

    for s in state_list:
        state = State(name=s)
        # Add senators for this state if we have them.
        if json.loads(data).get(s):
            state.senators = senators_from_json(json.loads(data).get(s))
        db.save(state)

    return


def senators_from_json(senator_data):
    """Parse senator data from json file for db."""
    senators = []

    for senator in senator_data:
        name = senator['name'],
        phone = senator['phone']

        senators.append(Senator(name=name[0], phone_number=phone))

    return senators


def zips_from_csv(zipcode_data):
    """Pull in all zipcodes, save in db."""
    # We can skip the first line from csv as it just defines columns
    all_zipcodes = []
    for zipcode in zipcode_data[1:]:
        # get zip and statename
        zcode = zipcode[1][0]
        statename = zipcode[1][3]
        zipcode_obj = Zipcode(zipcode=zcode, state=statename)
        all_zipcodes.append(zipcode_obj)
    db.session.bulk_save_objects(all_zipcodes)
    db.session.commit()

    return

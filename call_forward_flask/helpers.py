from models import (
    Senator,
    State,
    Zipcode,
)

def senator_lookup(state=None):
    senators_to_call = []
    # Handle missing state data, try to collect from caller.
    if not state:
        # TODO: direct back to key collection route
        print('OOPS')
    else:
        state_obj = State.query.filter_by(name=state).first()
        for senator in state_obj.senators.all():
            senators_to_call.append(senator)

    return senators_to_call

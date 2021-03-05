from call_forward_flask import app
from call_forward_flask.models import (
    Senator,
    State,
    Zipcode,
)

from flask import (
    Response,
    redirect,
    render_template,
    request,
    url_for,
)
from twilio.twiml.voice_response import VoiceResponse, Gather


@app.route('/')
def hello():
    """Very basic route to landing page."""
    return render_template('index.html')


@app.route('/callcongress/welcome', methods=['POST'])
def callcongress():
    """Verify or collect State intofrmation."""
    response = VoiceResponse()

    from_state = request.values.get('FromState', None)

    if from_state:
        gather = Gather(
            num_digits=1,
            action='/callcongress/set-state',
            method='POST',
            from_state=from_state,
        )
        gather.say(
            "Thank you for calling congress! It looks like "
            + "you\'re calling from {}. ".format(from_state)
            + "If this is correct, please press 1. Press 2 if "
            + "this is not your current state of residence."
        )
    else:
        gather = Gather(num_digits=5, action='/callcongress/state-lookup', method='POST')
        gather.say(
            "Thank you for calling Call Congress! If you wish to "
            + "call your senators, please enter your 5-digit zip code."
        )

    response.append(gather)
    return Response(str(response), 200, mimetype="application/xml")


@app.route('/callcongress/state-lookup', methods=['GET', 'POST'])
def state_lookup():
    """Look up state from given zipcode.

    Once state is found, redirect to call_senators for forwarding.
    """
    zip_digits = request.values.get('Digits', None)
    # NB: We don't do any error handling for a missing/erroneous zip code
    # in this sample application. You, gentle reader, should to handle that
    # edge case before deploying this code.
    zip_obj = Zipcode.query.filter_by(zipcode=zip_digits).first()

    return redirect(url_for('call_senators', state_id=zip_obj.state_id))


@app.route('/callcongress/collect-zip', methods=['GET', 'POST'])
def collect_zip():
    """If our state guess is wrong, prompt user for zip code."""
    response = VoiceResponse()

    gather = Gather(num_digits=5, action='/callcongress/state-lookup', method='POST')
    gather.say(
        "If you wish to call your senators, please " + "enter your 5-digit zip code."
    )
    response.append(gather)
    return Response(str(response), 200, mimetype="application/xml")


@app.route('/callcongress/set-state', methods=['GET', 'POST'])
def set_state():
    """Set state for senator call list.

    Set user's state from confirmation or user-provided Zip.
    Redirect to call_senators route.
    """
    # Get the digit pressed by the user
    digits_provided = request.values.get('Digits', None)

    # Set state if State correct, else prompt for zipcode.
    if digits_provided == '1':
        state = request.values.get('CallerState')
        state_obj = State.query.filter_by(name=state).first()
        if state_obj:
            return redirect(url_for('call_senators', state_id=int(state_obj.id)))

    return redirect(url_for('collect_zip'))


@app.route('/callcongress/call-senators/<state_id>', methods=['GET', 'POST'])
def call_senators(state_id):
    """Route for connecting caller to both of their senators."""
    senators = State.query.get(state_id).senators.all()

    response = VoiceResponse()

    first_call = senators[0]
    second_call = senators[1]

    response.say(
        "Connecting you to {}. ".format(first_call.name)
        + "After the senator's office ends the call, you will "
        + "be re-directed to {}.".format(second_call.name)
    )

    response.dial(
        first_call.phone, action=url_for('call_second_senator', senator_id=second_call.id)
    )

    return Response(str(response), 200, mimetype="application/xml")


@app.route('/callcongress/call-second-senator/<senator_id>', methods=['GET', 'POST'])
def call_second_senator(senator_id):
    """Forward the caller to their second senator."""
    senator = Senator.query.get(senator_id)

    response = VoiceResponse()
    response.say("Connecting you to {}.".format(senator.name))
    response.dial(senator.phone, action=url_for('end_call'))

    return Response(str(response), 200, mimetype="application/xml")


@app.route('/callcongress/goodbye', methods=['GET', 'POST'])
def end_call():
    """Thank user & hang up."""
    response = VoiceResponse()
    response.say(
        "Thank you for using Call Congress! " + "Your voice makes a difference. Goodbye."
    )
    response.hangup()
    return Response(str(response), 200, mimetype="application/xml")

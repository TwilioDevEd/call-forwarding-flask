import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from twilio.rest import TwilioRestClient

from call_forward_flask.config import (
    config_env_files,
    DevelopmentConfig
)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dev.sqlite'
db = SQLAlchemy()
client = TwilioRestClient(
    account=DevelopmentConfig.TWILIO_ACCOUNT_SID,
    token=DevelopmentConfig.TWILIO_AUTH_TOKEN
)


def prepare_app(environment='development', p_db=db):
    app.config.from_object(config_env_files[environment])
    p_db.init_app(app)
    # load views by importing them
    from call_forward_flask import views
    return app


def save_and_commit(item):
    db.session.add(item)
    db.session.commit()
db.save = save_and_commit

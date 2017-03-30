import os

from call_forward_flask.secrets import(
    TWILIO_ACCOUNT_SID,
    TWILIO_AUTH_TOKEN,
)

basedir = os.path.abspath(os.path.dirname(__file__))


class DefaultConfig(object):
    SECRET_KEY = 'secret-key'
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = ('sqlite:///' +
                               os.path.join(basedir, 'default.sqlite'))


class DevelopmentConfig(DefaultConfig):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = ('sqlite:///' +
                               os.path.join(basedir, 'dev.sqlite'))
    # Twilio API Key
    # Found at your Twilio dashboard https://www.twilio.com/console
    TWILIO_ACCOUNT_SID = TWILIO_ACCOUNT_SID
    TWILIO_AUTH_TOKEN = TWILIO_AUTH_TOKEN


class TestConfig(DefaultConfig):
    SQLALCHEMY_DATABASE_URI = ('sqlite:///' +
                               os.path.join(basedir, 'test.sqlite'))
    PRESERVE_CONTEXT_ON_EXCEPTION = False
    DEBUG = True

config_env_files = {
    'test': 'call_forward_flask.config.TestConfig',
    'development': 'call_forward_flask.config.DevelopmentConfig',
}

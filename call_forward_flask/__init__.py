from call_forward_flask.config import config_env_files
from flask import Flask

from flask.ext.sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dev.sqlite'
db = SQLAlchemy()


def prepare_app(environment='development', p_db=db):
    app.config.from_object(config_env_files[environment])
    p_db.init_app(app)
    # load views by importing them
    from . import views
    return app


def save_and_commit(item):
    db.session.add(item)
    db.session.commit()
db.save = save_and_commit

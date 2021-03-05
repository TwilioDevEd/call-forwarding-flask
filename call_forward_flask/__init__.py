
from call_forward_flask.config import (
    config_env_files,
)

from flask import Flask

from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dev.sqlite'
db = SQLAlchemy()
db.init_app(app)


environment = app.config.get('ENV', 'production')
app.config.from_object(config_env_files[environment])

# load views by importing them
from call_forward_flask import views  # noqa F401,F402

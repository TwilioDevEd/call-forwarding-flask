from flask.ext.script import Manager  
from flask.ext.migrate import Migrate, MigrateCommand  
from app import app, db
from parsers import senators_from_json

manager = Manager(app)  
migrate = Migrate(app, db)  
manager.add_command('db', MigrateCommand)

@manager.command
def dbseed():
    with open('senators.json') as senator_data:
        db.save(senators_from_json(senator_data.read()))

if __name__ == "__main__":  
    manager.run()

import csv

from flask_script import Manager
from flask_migrate import (
    Migrate,
    MigrateCommand,
)
from flask_migrate import upgrade as upgrade_database
from flask_migrate import migrate as migrate_database

from call_forward_flask import (
    app,
    db,
    parsers,
    prepare_app
)


prepare_app(environment='development')
migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)


@manager.command
def test():
    """Run the unit tests."""
    import sys
    import unittest
    prepare_app(environment='test')
    upgrade_database()
    migrate_database()

    tests = unittest.TestLoader().discover('.', pattern="*_tests.py")
    test_result = unittest.TextTestRunner(verbosity=2).run(tests)

    if not test_result.wasSuccessful():
        sys.exit(1)


@manager.command
def dbseed():
    with open('senators.json') as senator_data:
        parsers.data_from_json(senator_data.read())


@manager.command
def dbseed_zips():
    with open('free-zipcode-database.csv') as zip_data:
        zip_list = []
        reader = csv.reader(zip_data, delimiter=",")
        for line in enumerate(reader):
            zip_list.append(line)
        parsers.zips_from_csv(zip_list)


if __name__ == "__main__":
    manager.run()

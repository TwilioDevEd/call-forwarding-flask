import csv

from call_forward_flask import (
    app,
    db,
    parsers,
)

from flask_migrate import (
    Migrate,
    MigrateCommand,
)

from flask_script import Manager


migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)


@manager.command
def test():
    """Run the unit tests."""
    import sys
    import unittest

    tests = unittest.TestLoader().discover('.', pattern="*_tests.py")
    test_result = unittest.TextTestRunner(verbosity=2).run(tests)

    if not test_result.wasSuccessful():
        sys.exit(1)


@manager.command
def dbseed():
    """Seed db with states, senators and zip codes."""
    with open('senators.json') as senator_data:
        parsers.data_from_json(senator_data.read())
    with open('free-zipcode-database.csv') as zip_data:
        zip_list = []
        reader = csv.reader(zip_data, delimiter=",")
        for line in enumerate(reader):
            zip_list.append(line)
        parsers.zips_from_csv(zip_list)


if __name__ == "__main__":
    manager.run()

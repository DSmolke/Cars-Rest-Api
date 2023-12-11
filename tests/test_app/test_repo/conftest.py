import pytest

from app.env_variables import TESTS_URI, PORT

from migrations.mongodb.migration_mongodb import upgrade, downgrade, upgrade2


@pytest.fixture(autouse=True, scope='session')
def migrate_mongo_db():
    """
    Migrates the MongoDB database before running the tests.
    """
    downgrade(TESTS_URI, PORT)
    upgrade(TESTS_URI, PORT)


def pytest_sessionfinish(session, exitstatus):
    """
    @param session: The pytest session object
    @param exitstatus: The exit status of the pytest session

    This method is called when the pytest session finishes. It takes the pytest session object and the exit status as parameters. The method first calls the `downgrade` function passing
    * the `TESTS_URI` and `PORT` as arguments. Then, it calls the `upgrade2` function passing the `TESTS_URI` and `PORT` as arguments. Both functions perform some operations related to down
    *grading and upgrading the system.
    """
    downgrade(TESTS_URI, PORT)
    upgrade2(TESTS_URI, PORT)

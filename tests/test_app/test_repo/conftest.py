import pytest

from app.env_variables import TESTS_URI, PORT

from migrations.mongodb.migration_mongodb import upgrade, downgrade

@pytest.fixture(autouse=True, scope='session')
def migrate_mongo_db():
    """
    Before every test session
    """
    downgrade(TESTS_URI, PORT)
    upgrade(TESTS_URI, PORT)


def pytest_sessionfinish(session, exitstatus):
    """
    After every test session
    """
    downgrade(TESTS_URI, PORT)
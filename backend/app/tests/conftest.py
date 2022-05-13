import pytest
from faker import Faker

from backend.app import create_app
from backend.app.auth.models.user import User
from backend.app.auth.services.user.user_service import hash_password
from backend.app.configs import get_config

USER_COUNT = 5
fake = Faker()

pytest_plugins = [
    "app.tests.mock_functions"
]


@pytest.fixture(scope="session")
def app(test_configs):
    application = create_app(test_configs)

    application.app_context().push()
    yield application


@pytest.fixture(scope="session")
def test_configs():
    return get_config("test")


@pytest.fixture(scope="session")
def client(app):
    """A auth_provider client for the app."""
    return app.test_client()


@pytest.fixture(scope="session")
def created_users(app):
    users = []
    password = "testUserPassword123"
    for i in range(USER_COUNT):
        user = User(
            name=fake.name(),
            email=fake.email(),
            pw_hash=hash_password(password),
            roles=['admin']
        )
        user.save()
        users.append(user)

    yield users


@pytest.fixture(scope="session")
def fixture_user(created_users):
    yield created_users[0]

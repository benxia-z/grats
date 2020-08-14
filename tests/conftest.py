import pytest

from app import create_app, db
from app.models import User, Post
from config import Config


class TestConfig(Config):
    Testing = True
    SERVER_NAME = 'localhost:5000'
    SESSION_COOKIE_DOMAIN = False
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    WTF_CSRF_ENABLED = False

# Creating the Flask app
@pytest.fixture(scope='function')
def test_client():
    app = create_app(TestConfig)

    # Create testing client to mock user requests
    testing_client = app.test_client()

    # Create app context before running tests
    app_context = app.app_context()
    app_context.push()

    yield testing_client

    app_context.pop()

# Initializing the database
@pytest.fixture(scope='function')
def init_db():
    db.create_all()

    # Create test users
    user1 = User(username='john', email='john@example.com')
    user1.set_password('cat')
    user2 = User(username='susan', email='susan@example.com')
    user2.set_password('dog')
    db.session.add(user1)
    db.session.add(user2)

    db.session.commit()

    yield db

    db.drop_all()

# Creating a new user
@pytest.fixture(scope='module')
def new_user():
    user = User(username='john', email='john@example.com')
    user.set_password('cat')
    return user

import pytest
import unittest
from datetime import datetime
from werkzeug.security import generate_password_hash

from App.main import create_app
from App.database import db, create_db
from App.models import User, Admin, Student, Group, GroupRequest, StudentGroup, Lot, LotGroup, RFPRequest, Bid, Evaluation
from App.controllers import *

@pytest.fixture(autouse=True, scope="module")
def empty_db():
    app = create_app({'TESTING': True, 'SQLALCHEMY_DATABASE_URI': 'sqlite:///test.db'})
    create_db()
    yield app.test_client()
    db.drop_all()

def test_authenticate():
    user = create_user("bob", "bobpass")
    assert login("bob", "bobpass") != None

class UsersIntegrationTests(unittest.TestCase):
    def test_user_children_are_users(self):
        admin = Admin("jack", "jackpass")
        db.session.add(admin)
        student = Student("cooper", "cooperpass")
        db.session.add(student)
        db.session.commit()
        users_json = get_all_users_json()
        self.assertListEqual([{"id":1, "username":"bob"}, {"id":2, "username":"jack", "role":"admin"}, {"id":3, "username":"cooper", "role":"student"}], users_json)

    def test_create_user(self):
        user = create_user("rick", "bobpass")
        assert user.username == "rick"

    def test_get_all_users_json(self):
        users_json = get_all_users_json()
        self.assertListEqual([{"id":1, "username":"bob"}, {"id":2, "username":"rick"}], users_json)

    # Tests data changes in the database
    def test_update_user(self):
        update_user(1, "ronnie")
        user = get_user(1)
        assert user.username == "ronnie"
    

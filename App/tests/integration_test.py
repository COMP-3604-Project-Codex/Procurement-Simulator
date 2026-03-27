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

@pytest.mark.run(order=1)
def test_authenticate():
    user = create_user("bob", "bobpass")
    assert login("bob", "bobpass") != None

class UsersIntegrationTests(unittest.TestCase):
    @pytest.mark.run(order=2)
    def test_user_children_are_users(self):
        admin = Admin("jack", "jackpass")
        db.session.add(admin)
        student = Student("cooper", "cooperpass")
        db.session.add(student)
        db.session.commit()
        users_json = get_all_users_json()
        self.assertListEqual([{"id":1, "username":"bob"}, {"id":2, "username":"jack", "role":"admin"}, {"id":3, "username":"cooper", "role":"student"}], users_json)

    # Tests data changes in the database
    @pytest.mark.run(order=3)
    def test_update_user(self):
        update_user(1, "ronnie")
        user = get_user(1)
        assert user.username == "ronnie"

class Workflow1IntegrationTests(unittest.TestCase):
    @pytest.mark.run(order=4)
    def test_creating_lots(self):
        db.drop_all()
        create_db()
        create_lot("GIS Lab", 20, 160000.00)
        create_lot("Government Office Lab", 12, 110000.00)
        lots_json = get_all_lots_json()
        self.assertListEqual([
        {
            'id': 1,
            'labType': "GIS Lab",
            'labSize': 20,
            'budget': 160000.00
        },
        {
            'id': 2,
            'labType': "Government Office Lab",
            'labSize': 12,
            'budget': 110000.00
        }
        ], lots_json)

    @pytest.mark.run(order=5)
    def test_edit_lots(self):
        lot = get_lot(1)
        assert lot.budget == 160000.00
        edit_lot(1, budget=170000.00)
        lot = get_lot(1)
        assert lot.budget == 170000.00

    @pytest.mark.run(order=6)
    def test_remove_lot(self):
        lot = get_lot(1)
        assert not lot == None
        remove_lot(1)
        lot = get_lot(1)
        assert lot == None



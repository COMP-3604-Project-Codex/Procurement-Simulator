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
        create_admin("bob", "bobpass")
        create_lot("GIS Lab", 20, 160000.00)
        create_lot("Government Office Lab", 12, 110000.00)
        lots_json = get_all_lots_json()
        self.assertListEqual([
        {
            'id': 1,
            'name': "Lot 1",
            'labType': "GIS Lab",
            'labSize': 20,
            'budget': 160000.00
        },
        {
            'id': 2,
            'name': "Lot 2",
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

class Workflow2IntegrationTests(unittest.TestCase):
    @pytest.mark.run(order=7)
    def test_create_groupRequest(self):
        remove_lot(2)
        create_lot("GIS Lab", 20, 160000.00)
        create_lot("Government Office Lab", 12, 110000.00)
        create_lot("University Computer Lab", 40, 250000.00)
        create_lot("Data Center", 1000, 25000000.00)

        create_student("jack", "jackpass")
        create_student("cooper", "cooperpass")
        create_student("john", "johnpass")
        create_student("tony", "tonypass")

        create_student("peper", "peperpass")
        create_student("steve", "stevepass")
        create_student("clint", "clintpass")
        create_student("bruce", "brucepass")

        attempt = create_groupRequest("TechNova Solution", [1,2,3,4])
        assert attempt["status"] == "good"

        groupReq = get_groupRequest(attempt["id"])
        self.assertDictEqual({
            'id': 1,
            'groupName': "TechNova Solution",
            'members': [1,2,3,4]
        }, groupReq.get_json())

    @pytest.mark.run(order=8)
    def test_trying_to_create_group_request_with_a_duplicate_member(self):
        attempt = create_groupRequest("ANK Productions", [1,2,3,4])
        assert attempt["status"] == "bad"
        assert attempt["duplicates"] == [1,2,3,4]

        attempt = create_groupRequest("ANK Productions", [1,5,6,7])
        assert attempt["status"] == "bad"
        assert attempt["duplicates"] == [1]

        attempt = create_groupRequest("ANK Productions", [1,5,2,7])
        assert attempt["status"] == "bad"
        assert attempt["duplicates"] == [1,2]

        attempt = create_groupRequest("ANK Productions", [1,3,2,7])
        assert attempt["status"] == "bad"
        assert attempt["duplicates"] == [1,3,2]

class Workflow3IntegrationTests(unittest.TestCase):
    @pytest.mark.run(order=9)
    def test_approving_groupReuests(self):
        attempt = create_groupRequest("ANK Productions", [5,6,7,8])
        assert attempt["status"] == "good"

        groupReq = get_groupRequest(attempt["id"])
        self.assertDictEqual({
            'id': 2,
            'groupName': "ANK Productions",
            'members': [5,6,7,8]
        }, groupReq.get_json())

        groupReq = get_groupRequest(1)

        group = create_group(groupReq.groupName)
        assert group.groupName == "G1 TechNova Solution"

        for member in groupReq.members:
            add_studentGroup(member, group.id)
        
        self.assertListEqual([
            {
                'studentID': 1,
                'groupID': 1
            },
            {
                'studentID': 2,
                'groupID': 1
            },
            {
                'studentID': 3,
                'groupID': 1
            },
            {
                'studentID': 4,
                'groupID': 1
            }
        ], get_all_studentGroups_json())

        add_lotGroup(1, group.id)
        add_lotGroup(2, group.id)

        self.assertListEqual([
            {
                'lotID': 1,
                'groupID': 1
            },
            {
                'lotID': 2,
                'groupID': 1
            }
        ], get_all_lotGroups_json())

        removed = remove_groupRequest(1)
        assert removed == True

        groupReq = get_groupRequest(1)
        assert not groupReq

    @pytest.mark.run(order=10)
    def test_rejecting_a_group_request(self):
        rejected = remove_groupRequest(2)
        assert rejected
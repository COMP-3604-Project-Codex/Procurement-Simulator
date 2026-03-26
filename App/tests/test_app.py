import pytest
import unittest
from datetime import datetime
from werkzeug.security import generate_password_hash

from App.main import create_app
from App.database import db, create_db
from App.models import User, Admin, Student, Group, GroupRequest, StudentGroup, Lot, LotGroup, RFPRequest, Bid, Evaluation


'''
    Unit Tests
'''

class AdminUnitTests(unittest.TestCase):

    def test_new_admin(self):
        admin = Admin("alice", "alicepass")
        assert admin.username == "alice"

    def test_admin_get_json(self):
        admin = Admin("alice", "alicepass")
        admin_json = admin.get_json()
        assert admin_json["username"] == "alice"
        assert admin_json["role"] == "admin"

    def test_admin_hashed_password(self):
        admin = Admin("alice", "alicepass")
        assert admin.password != "alicepass"

    def test_admin_check_password(self):
        admin = Admin("alice", "alicepass")
        assert admin.check_password("alicepass")

    def test_admin_is_admin(self):
        admin = Admin("alice", "alicepass")
        assert admin.is_admin()

    def test_admin_is_not_student(self):
        admin = Admin("alice", "alicepass")
        assert not admin.is_student()


class StudentUnitTests(unittest.TestCase):

    def test_new_student(self):
        student = Student("bob", "bobpass")
        assert student.username == "bob"

    def test_student_get_json(self):
        student = Student("bob", "bobpass")
        student_json = student.get_json()
        assert student_json["username"] == "bob"
        assert student_json["role"] == "student"

    def test_student_hashed_password(self):
        student = Student("bob", "bobpass")
        assert student.password != "bobpass"

    def test_student_check_password(self):
        student = Student("bob", "bobpass")
        assert student.check_password("bobpass")

    def test_student_is_student(self):
        student = Student("bob", "bobpass")
        assert student.is_student()

    def test_student_is_not_admin(self):
        student = Student("bob", "bobpass")
        assert not student.is_admin()


class GroupUnitTests(unittest.TestCase):

    def test_new_group(self):
        group = Group("Algorithms")
        assert group.groupName == "Algorithms"

    def test_group_get_json(self):
        group = Group("Algorithms")
        group_json = group.get_json()
        assert group_json["groupName"] == "Algorithms"


class GroupRequestUnitTests(unittest.TestCase):

    def test_new_group_request(self):
        group_request = GroupRequest("Algorithms", [1, 2, 3])
        assert group_request.groupName == "Algorithms"

    def test_group_request_members(self):
        group_request = GroupRequest("Algorithms", [1, 2, 3])
        assert group_request.members == [1, 2, 3]

    def test_group_request_get_json(self):
        group_request = GroupRequest("Algorithms", [1, 2, 3])
        group_json = group_request.get_json()
        assert group_json["groupName"] == "Algorithms"
        assert group_json["members"] == [1, 2, 3]


class StudentGroupUnitTests(unittest.TestCase):

    def test_new_student_group(self):
        student_group = StudentGroup(1, 2)
        assert student_group.studentID == 1
        assert student_group.groupID == 2

    def test_student_group_get_json(self):
        student_group = StudentGroup(1, 2)
        sg_json = student_group.get_json()
        self.assertDictEqual(sg_json, {"studentID": 1, "groupID": 2})


class LotUnitTests(unittest.TestCase):

    def test_new_lot(self):
        lot = Lot("Biology", 30, 5000.00)
        assert lot.labType == "Biology"

    def test_lot_lab_size(self):
        lot = Lot("Biology", 30, 5000.00)
        assert lot.labSize == 30

    def test_lot_budget(self):
        lot = Lot("Biology", 30, 5000.00)
        assert lot.budget == 5000.00

    def test_lot_get_json(self):
        lot = Lot("Biology", 30, 5000.00)
        lot_json = lot.get_json()
        self.assertDictEqual(lot_json, {
            "id": None,
            "labType": "Biology",
            "labSize": 30,
            "budget": 5000.00
        })

    def test_lot_budget_comparison(self):
        lot = Lot("Biology", 30, 5000.00)
        assert 4999.99 < lot.budget
        assert 5000.01 > lot.budget


class LotGroupUnitTests(unittest.TestCase):

    def test_new_lot_group(self):
        lot_group = LotGroup(1, 2)
        assert lot_group.lotID == 1
        assert lot_group.groupID == 2

    def test_lot_group_get_json(self):
        lot_group = LotGroup(1, 2)
        lg_json = lot_group.get_json()
        self.assertDictEqual(lg_json, {"lotID": 1, "groupID": 2})


class RFPRequestUnitTests(unittest.TestCase):

    def test_new_rfp_request(self):
        rfp = RFPRequest(1, 2, {"detail": "some spec"})
        assert rfp.groupID == 1
        assert rfp.lotID == 2

    def test_rfp_request_specs(self):
        specs = {"detail": "some spec", "budget": 1000}
        rfp = RFPRequest(1, 2, specs)
        assert rfp.specs == specs

    def test_rfp_request_get_json(self):
        specs = {"detail": "some spec"}
        rfp = RFPRequest(1, 2, specs)
        rfp_json = rfp.get_json()
        assert rfp_json["groupID"] == 1
        assert rfp_json["lotID"] == 2
        assert rfp_json["specs"] == specs


class BidUnitTests(unittest.TestCase):

    def test_new_bid(self):
        bid = Bid(1, 2, 3, "http://example.com/doc")
        assert bid.lotID == 1
        assert bid.sourceGroupID == 2
        assert bid.receipientGroupID == 3

    def test_bid_document_link(self):
        bid = Bid(1, 2, 3, "http://example.com/doc")
        assert bid.bidDocumentLink == "http://example.com/doc"

    def test_bid_timestamp_auto_set(self):
        bid = Bid(1, 2, 3, "http://example.com/doc")
        assert isinstance(bid.timestamp, datetime)

    def test_bid_timestamp_is_recent(self):
        bid = Bid(1, 2, 3, "http://example.com/doc")
        delta = datetime.utcnow() - bid.timestamp
        assert delta.seconds < 5

    def test_bid_get_json(self):
        bid = Bid(1, 2, 3, "http://example.com/doc")
        bid_json = bid.get_json()
        assert bid_json["lotID"] == 1
        assert bid_json["sourceGroupID"] == 2
        assert bid_json["receipientGroupID"] == 3
        assert bid_json["bidDocumentLink"] == "http://example.com/doc"
        assert "timestamp" in bid_json


class EvaluationUnitTests(unittest.TestCase):

    def test_new_evaluation(self):
        evaluation = Evaluation(1, 2, {"score": 85})
        assert evaluation.sourceGroupID == 1
        assert evaluation.receipientGroupID == 2

    def test_evaluation_details(self):
        details = {"score": 85, "comments": "Good work"}
        evaluation = Evaluation(1, 2, details)
        assert evaluation.evaluationDetails == details

    def test_evaluation_get_json(self):
        details = {"score": 85}
        evaluation = Evaluation(1, 2, details)
        eval_json = evaluation.get_json()
        assert eval_json["sourceGroupID"] == 1
        assert eval_json["receipientGroupID"] == 2
        assert eval_json["evaluationDetails"] == details

'''
    Integration Tests
'''

# This fixture creates an empty database for the test and deletes it after the test
# scope="class" would execute the fixture once and resued for all methods in the class
# @pytest.fixture(autouse=True, scope="module")
# def empty_db():
#     app = create_app({'TESTING': True, 'SQLALCHEMY_DATABASE_URI': 'sqlite:///test.db'})
#     create_db()
#     yield app.test_client()
#     db.drop_all()


# def test_authenticate():
#     user = create_user("bob", "bobpass")
#     assert login("bob", "bobpass") != None

# class UsersIntegrationTests(unittest.TestCase):

#     def test_create_user(self):
#         user = create_user("rick", "bobpass")
#         assert user.username == "rick"

#     def test_get_all_users_json(self):
#         users_json = get_all_users_json()
#         self.assertListEqual([{"id":1, "username":"bob"}, {"id":2, "username":"rick"}], users_json)

#     # Tests data changes in the database
#     def test_update_user(self):
#         update_user(1, "ronnie")
#         user = get_user(1)
#         assert user.username == "ronnie"
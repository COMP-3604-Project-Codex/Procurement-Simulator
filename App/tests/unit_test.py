import pytest
import unittest
from datetime import datetime
from werkzeug.security import generate_password_hash

from App.main import create_app
from App.database import db, create_db
from App.models import User, Admin, Student, Group, StudentGroup, Lot, LotGroup, Bid, Evaluation, RFP


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
            "name": None,
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

class RFPUnitTests(unittest.TestCase):
    def test_new_RFP(self):
        rfp = RFP(1, 10)
        assert rfp
        assert rfp.groupID == 1
        assert rfp.lotID == 10
    
    def test_RFP_get_json(self):
        rfp = RFP(1, 10)
        assert rfp

        self.assertDictEqual({
            'groupID': 1,
            'lotID': 10,
            'status': None,
            'Type': None,
            'Screen Size & Resolution': None,
            'Operating System(s)': None,
            'CPU': None,
            'Memory (RAM)': None,
            'Hard Drive': None,
            'Graphics': None,
            'External Peripherals': None,
            'Features': None,
            'I/O': None
        }, rfp.get_json())

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
        sourceGroupID = 1
        receipientGroupID = 2
        bidID = 2
        lotID = 1
        specsMet = 5
        presentation = 3
        professionalism = 2
        budget = 4

        evaluation = Evaluation(sourceGroupID, receipientGroupID, bidID, lotID, specsMet, presentation, professionalism, budget)
        assert evaluation
        assert evaluation.overallScore == 5.6

    def test_evaluation_get_json(self):
        sourceGroupID = 1
        receipientGroupID = 2
        bidID = 2
        lotID = 1
        specsMet = 5
        presentation = 3
        professionalism = 2
        budget = 4

        evaluation = Evaluation(sourceGroupID, receipientGroupID, bidID, lotID, specsMet, presentation, professionalism, budget)

        self.assertDictEqual({
            'id': None,
            'sourceGroupID': 1,
            'receipientGroupID': 2,
            'bidID': 2,
            'lotID': 1,
            'overallScore': 5.6
        }, evaluation.get_json())
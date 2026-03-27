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

class Workflow4IntegrationTests(unittest.TestCase):
    @pytest.mark.run(order=11)
    def test_remove_group(self):
        group = get_group(1)
        entries = db.session.scalars(db.select(StudentGroup).filter_by(groupID = group.id)).all()

        for entry in entries:
            removed = remove_studentGroup(entry.studentID, entry.groupID)
            assert removed
        
        entries = db.session.scalars(db.select(LotGroup).filter_by(groupID = group.id)).all()

        for entry in entries:
            removed = remove_lotGroup(entry.lotID, entry.groupID)
            assert removed

        removed = remove_group(group.id)
        assert removed

class Workflow5IntegrationTests(unittest.TestCase):
    @pytest.mark.run(order=12)
    def test_save_rfp_details(self):
        attempt = create_groupRequest("TechNova Solution", [1,2,3,4])
        assert attempt["status"] == "good"

        attempt = create_groupRequest("ANK Productions", [5,6,7,8])
        assert attempt["status"] == "good"

        for i in range(1, 3):
            groupReq = get_groupRequest(i)

            group = create_group(groupReq.groupName)

            for member in groupReq.members:
                add_studentGroup(member, group.id)

            if i == 1:
                add_lotGroup(1, group.id)
                add_lotGroup(2, group.id)
            else:
                add_lotGroup(3, group.id)
                add_lotGroup(4, group.id)

            removed = remove_groupRequest(i)
        
        self.assertDictEqual({
            "deviceType": "",
            "resolution": "",
            "os": "",
            "cpu": "",
            "ram": "",
            "drive": "",
            "gpu": "",
            "peripherals": "",
            "features": "",
            "io": "" 
        }, get_lotRFP_details_json(1))
    
        details1 = {
            "deviceType": "Workstation/Laptop/Tablet",
            "resolution": "",
            "os": "Mac/Windows/Android/IOS/Linux/Chromium",
            "cpu": "Core and frequency range eg (quad-core @ 2.2 - 3.0 GHz)",
            "ram": "",
            "drive": "",
            "gpu": "",
            "peripherals": "",
            "features": "",
            "io": "" 
        }

        lot = edit_lotRFP_details(1, details1)

        self.assertDictEqual({
            "deviceType": "Workstation/Laptop/Tablet",
            "resolution": "",
            "os": "Mac/Windows/Android/IOS/Linux/Chromium",
            "cpu": "Core and frequency range eg (quad-core @ 2.2 - 3.0 GHz)",
            "ram": "",
            "drive": "",
            "gpu": "",
            "peripherals": "",
            "features": "",
            "io": "" 
        }, get_lotRFP_details_json(lot.id))

        details2 = {
            "deviceType": "",
            "resolution": "",
            "os": "",
            "cpu": "",
            "ram": "",
            "drive": "HDD/SSD, speed and capacity range, (list if secondary storage)",
            "gpu": "",
            "peripherals": "Mouse keyboard, touchpad, gamepad, headset, speakers, webcam, adapters, hubs, eGPU, drawing tablet",
            "features": "Touch screen, WIFI version, bluetooth, Capture Card, Integrated Speakers, Integrated Webcam, Fingerprint reader, LTE",
            "io": "Optical Drive, USB Type-C, USB 3, USB 4, HDMI input, HDMI out, ethernet, Display port, thunderbolt, SD card reader, audio ports" 
        }

        lot = edit_lotRFP_details(2, details2)

        self.assertDictEqual({
            "deviceType": "",
            "resolution": "",
            "os": "",
            "cpu": "",
            "ram": "",
            "drive": "HDD/SSD, speed and capacity range, (list if secondary storage)",
            "gpu": "",
            "peripherals": "Mouse keyboard, touchpad, gamepad, headset, speakers, webcam, adapters, hubs, eGPU, drawing tablet",
            "features": "Touch screen, WIFI version, bluetooth, Capture Card, Integrated Speakers, Integrated Webcam, Fingerprint reader, LTE",
            "io": "Optical Drive, USB Type-C, USB 3, USB 4, HDMI input, HDMI out, ethernet, Display port, thunderbolt, SD card reader, audio ports" 
        }, get_lotRFP_details_json(lot.id))

    @pytest.mark.run(order=13)
    def test_submit_rfp_details(self):
        lot = get_lot(1)
        attempt = create_rfpRequest(1, lot.id, lot.specs)
        self.assertDictEqual({
            "id": (1, 1),
            "status": "good",
            "message": "RFP Request was sent successfully"
        }, attempt)

        lot = get_lot(2)
        attempt = create_rfpRequest(1, lot.id, lot.specs)
        self.assertDictEqual({
            "id": (1, 2),
            "status": "good",
            "message": "RFP Request was sent successfully"
        }, attempt)
    
    @pytest.mark.run(order=14)
    def test_submit_duplicate_rfp_details(self):
        lot = get_lot(1)
        attempt = create_rfpRequest(1, lot.id, lot.specs)
        self.assertDictEqual({
            "id": (0, 0),
            "status": "bad",
            "message": "You already submitted an rfp request for Lot1"
        }, attempt)

class Workflow6IntegrationTests(unittest.TestCase):
    @pytest.mark.run(order=15)
    def test_approve_rfp_Request(self):
        rfpRequest = get_rfpRequest(1, 1)

        create_rfp(rfpRequest.groupID, rfpRequest.lotID, rfpRequest.specs)

        rfp = get_rfp(1, 1)

        self.assertDictEqual({
            'groupID': 1,
            'lotID': 1,
            'specs': {
                "deviceType": "Workstation/Laptop/Tablet",
                "resolution": "",
                "os": "Mac/Windows/Android/IOS/Linux/Chromium",
                "cpu": "Core and frequency range eg (quad-core @ 2.2 - 3.0 GHz)",
                "ram": "",
                "drive": "",
                "gpu": "",
                "peripherals": "",
                "features": "",
                "io": "" 
            }
        }, rfp.get_json())

        removed = remove_rfpRequest(1, 1)
        assert removed

    @pytest.mark.run(order=16)
    def test_reject_rfp_Request(self):
        removed = remove_rfpRequest(1, 2)
        assert removed

        reqs = get_all_rfpRequests()
        assert not reqs

        rfps = get_all_rfps()
        assert len(rfps) == 1
import pytest
import unittest
from datetime import datetime
from werkzeug.security import generate_password_hash

from App.main import create_app
from App.database import db, create_db
from App.models import User, Admin, Student, Group, StudentGroup, Lot, LotGroup, Bid, Evaluation, RFP
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

        groupName = "TechNova Solution"
        members = [1,2,3,4]

        group = create_group(groupName)
        group = get_group(1)
        self.assertDictEqual({
            'id': 1,
            'groupName': "G1 TechNova Solution",
            'status': "requested"
        }, group.get_json())

        for member in members:
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
            },
        ], get_all_studentGroups_json())

    @pytest.mark.run(order=8)
    def test_trying_to_create_group_request_with_a_duplicate_member(self):
        groupName = "ANK Productions"
        members = [1,2,3,4]

        duplicates = []

        for member in members:
            existing = db.session.scalars(db.select(StudentGroup).filter_by(studentID = member)).first()
            if existing:
                duplicates.append(member)
        
        assert duplicates == [1,2,3,4]

        members = [5,6,7,8]
        group = create_group(groupName)

        for member in members:
            add_studentGroup(member, group.id)

class Workflow3IntegrationTests(unittest.TestCase):
    @pytest.mark.run(order=9)
    def test_approving_groupReuests(self):
        groupID = 1
        Lot1ID = 1
        Lot2ID = 2
        group = get_group(groupID)
        add_lotGroup(Lot1ID, group.id)
        add_lotGroup(Lot2ID, group.id)

        group.status = "approved"
        db.session.commit()

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

        group = get_group(1)
        assert group.status == "approved"

    @pytest.mark.run(order=10)
    def test_rejecting_a_group_request(self):
        groupID = 2

        entries = db.session.scalars(db.select(StudentGroup).filter_by(groupID = groupID)).all()

        for entry in entries:
            removed = remove_studentGroup(entry.studentID, groupID)
            assert removed

        entries = db.session.scalars(db.select(LotGroup).filter_by(groupID = groupID)).all()

        for entry in entries:
            removed = remove_lotGroup(entry.lotID, groupID)
            assert removed

        removed = remove_group(groupID)
        assert removed

class Workflow4IntegrationTests(unittest.TestCase):
    @pytest.mark.run(order=11)
    def test_remove_group(self):
        groupID = 1

        entries = db.session.scalars(db.select(StudentGroup).filter_by(groupID = groupID)).all()

        for entry in entries:
            removed = remove_studentGroup(entry.studentID, groupID)
            assert removed

        entries = db.session.scalars(db.select(LotGroup).filter_by(groupID = groupID)).all()

        for entry in entries:
            removed = remove_lotGroup(entry.lotID, groupID)
            assert removed

        removed = remove_group(groupID)
        assert removed


class Workflow5IntegrationTests(unittest.TestCase):
    @pytest.mark.run(order=12)
    def test_save_rfp_details(self):
        lotID = 1
        deviceType = "Workstation/Laptop/Tablet"
        resolution = ""
        os = "Mac/Windows/Android/IOS/Linux/Chromium"
        cpu = "Core and frequency range eg (quad-core @ 2.2 - 3.0 GHz)"
        ram = ""
        drive = ""
        gpu = ""
        peripherals = ""
        features = ""
        io = ""

        lot = edit_lotRFP_details(lotID, deviceType=deviceType, os=os, cpu=cpu)
        assert lot.deviceType == "Workstation/Laptop/Tablet"
        assert lot.resolution == ""
        assert lot.os == "Mac/Windows/Android/IOS/Linux/Chromium"
        assert lot.cpu == "Core and frequency range eg (quad-core @ 2.2 - 3.0 GHz)"
        assert lot.ram == ""
        assert lot.drive == ""
        assert lot.gpu == ""
        assert lot.peripherals == ""
        assert lot.features == ""
        assert lot.io == ""

        lotID = 2
        deviceType = ""
        resolution = ""
        os = ""
        cpu = ""
        ram = ""
        drive = "HDD/SSD, speed and capacity range, (list if secondary storage)"
        gpu = "Integrated/Dedicated with memory range"
        peripherals = ""
        features = "Touch screen, WIFI version, bluetooth, Capture Card, Integrated Speakers, Integrated Webcam, Fingerprint reader, LTE"
        io = ""

        lot = edit_lotRFP_details(lotID, drive=drive, gpu=gpu, features=features)
        assert lot.deviceType == ""
        assert lot.resolution == ""
        assert lot.os == ""
        assert lot.cpu == ""
        assert lot.ram == ""
        assert lot.drive == "HDD/SSD, speed and capacity range, (list if secondary storage)"
        assert lot.gpu == "Integrated/Dedicated with memory range"
        assert lot.peripherals == ""
        assert lot.features == "Touch screen, WIFI version, bluetooth, Capture Card, Integrated Speakers, Integrated Webcam, Fingerprint reader, LTE"
        assert lot.io == ""


    @pytest.mark.run(order=13)
    def test_submit_rfp_details(self):
        lotID = 1
        groupID = 1

        rfp = create_rfp(lotID, groupID)

        lot = get_lot(lotID)

        rfp.deviceType = lot.deviceType
        rfp.resolution = lot.resolution
        rfp.os = lot.os
        rfp.cpu = lot.cpu
        rfp.ram = lot.ram
        rfp.drive = lot.drive
        rfp.gpu = lot.gpu
        rfp.peripherals = lot.peripherals
        rfp.features = lot.features
        rfp.io = lot.io

        db.session.commit()

        rfp = get_rfp(groupID, lotID)
        assert rfp.deviceType == "Workstation/Laptop/Tablet"
        assert rfp.resolution == ""
        assert rfp.os == "Mac/Windows/Android/IOS/Linux/Chromium"
        assert rfp.cpu == "Core and frequency range eg (quad-core @ 2.2 - 3.0 GHz)"
        assert rfp.ram == ""
        assert rfp.drive == ""
        assert rfp.gpu == ""
        assert rfp.peripherals == ""
        assert rfp.features == ""
        assert rfp.io == ""
        assert rfp.status == "requested"
        
    
    @pytest.mark.run(order=14)
    def test_submit_duplicate_rfp_details(self):
        lotID = 1
        groupID = 1

        rfp = db.session.scalars(db.select(RFP).filter_by(groupID=groupID, lotID=lotID)).first()
        assert rfp
        assert rfp.status == "requested"

        lotID = 2

        rfp = create_rfp(groupID, lotID)
        assert rfp

        lot = get_lot(lotID)

        rfp.deviceType = lot.deviceType
        rfp.resolution = lot.resolution
        rfp.os = lot.os
        rfp.cpu = lot.cpu
        rfp.ram = lot.ram
        rfp.drive = lot.drive
        rfp.gpu = lot.gpu
        rfp.peripherals = lot.peripherals
        rfp.features = lot.features
        rfp.io = lot.io

        db.session.commit()

        rfp = get_rfp(groupID, lotID)
        assert rfp.deviceType == ""
        assert rfp.resolution == ""
        assert rfp.os == ""
        assert rfp.cpu == ""
        assert rfp.ram == ""
        assert rfp.drive == "HDD/SSD, speed and capacity range, (list if secondary storage)"
        assert rfp.gpu == "Integrated/Dedicated with memory range"
        assert rfp.peripherals == ""
        assert rfp.features == "Touch screen, WIFI version, bluetooth, Capture Card, Integrated Speakers, Integrated Webcam, Fingerprint reader, LTE"
        assert rfp.io == ""
        assert rfp.status == "requested"

class Workflow6IntegrationTests(unittest.TestCase):
    @pytest.mark.run(order=15)
    def test_approve_rfp_Request(self):
        lotID = 1
        groupID = 1

        rfp = get_rfp(groupID, lotID)
        rfp.status = "approved"
        db.session.commit()

        rfp = get_rfp(groupID, lotID)
        assert rfp.status == "approved"

    @pytest.mark.run(order=16)
    def test_reject_rfp_Request(self):
        groupID = 1
        lotID = 2

        removed = remove_rfp(groupID, lotID)
        assert removed

class Workflow7IntegrationTests(unittest.TestCase):
    @pytest.mark.run(order=17)
    def test_remove_rfp(self):
        groupID = 1
        lotID = 1

        removed = remove_rfp(groupID, lotID)
        assert removed
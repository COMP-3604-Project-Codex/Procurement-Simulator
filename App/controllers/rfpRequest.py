from App.models import RFPRequest
from App.database import db

def create_rfpRequest(groupID, lotID, specs):
    duplicate = False

    existing = db.session.scalars(db.select(RFPRequest).filter_by(lotID = lotID)).first()
    if existing:
        duplicate = True

    if not duplicate:
        newreq = RFPRequest(groupID, lotID, specs)
        db.session.add(newreq)
        db.session.commit()
        return {
            "id": (groupID, lotID),
            "status": "good",
            "message": "RFP Request was sent successfully"
        }
    else:
        return {
            "id": (0, 0),
            "status": "bad",
            "message": f"You already submitted a group request for Lot{lotID}"
        }

def get_rfpRequest(id):
    return db.session.get(RFPRequest, id)

def get_all_rfpRequests():
    return db.session.scalars(db.select(GroupRequest)).all()

def get_all_rfpRequests_json():
    reqs = get_all_rfpRequests()
    if not reqs:
        return []
    reqs = [req.get_json() for req in reqs]
    return reqs

def remove_rfpRequest(id):
    req = get_rfpRequest(id)
    if req:
        db.session.delete(req)
        db.session.commit()
        return True
    return False
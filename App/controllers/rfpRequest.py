from App.models import RFPRequest, RFP
from App.database import db

def create_rfpRequest(groupID, lotID, specs):
    duplicate = False
    approved = False

    existing = db.session.scalars(db.select(RFPRequest).filter_by(lotID = lotID)).first()
    if existing:
        duplicate = True

    appr = db.session.scalars(db.select(RFP).filter_by(lotID = lotID)).first()
    if appr:
        approved = True

    if not duplicate and not approved:
        newreq = RFPRequest(groupID, lotID, specs)
        db.session.add(newreq)
        db.session.commit()
        return {
            "id": (groupID, lotID),
            "status": "good",
            "message": "RFP Request was sent successfully"
        }
    elif duplicate:
        return {
            "id": (0, 0),
            "status": "bad",
            "message": f"You already submitted an rfp request for Lot{lotID}"
        }
    elif approved:
        return {
            "id": (0, 0),
            "status": "bad",
            "message": f"You already have an approved RFP in the gallery for Lot{lotID}"
        }
    else:
        return None

def get_rfpRequest(groupID, lotID):
    return db.session.get(RFPRequest, (groupID, lotID))

def get_all_rfpRequests():
    return db.session.scalars(db.select(RFPRequest)).all()

def get_all_rfpRequests_json():
    reqs = get_all_rfpRequests()
    if not reqs:
        return []
    reqs = [req.get_json() for req in reqs]
    return reqs

def remove_rfpRequest(groupID, lotID):
    req = get_rfpRequest(groupID, lotID)
    if req:
        db.session.delete(req)
        db.session.commit()
        return True
    return False
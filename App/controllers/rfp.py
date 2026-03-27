from App.models import RFP
from App.database import db

def create_rfp(groupID, lotID):
    rfp = RFP(groupID, lotID)
    db.session.add(rfp)
    db.session.commit()
    return rfp

def get_rfp(groupID, lotID):
    return db.session.get(RFP, (groupID, lotID))

def get_all_rfps():
    return db.session.scalars(db.select(RFP)).all()

def get_all_rfps_json():
    rfps = get_all_rfps()
    if not rfps:
        return []
    rfps = [rfp.get_json() for rfp in rfps]
    return rfps

def remove_rfp(groupID, lotID):
    rfp = get_rfp(groupID, lotID)
    if rfp:
        db.session.delete(rfp)
        db.session.commit()
        return True
    return False
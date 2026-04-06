from App.models import RFP, Bid
from App.database import db
from .lot import get_lot
from .bid import remove_bid

def create_rfp(groupID, lotID):
    rfp = RFP(groupID, lotID)
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
    
    db.session.add(rfp)
    db.session.commit()
    return rfp

def approve_rfp(groupID, lotID):
    rfp = get_rfp(groupID, lotID)
    rfp.status = "approved"
    db.session.commit()

def get_rfp(groupID, lotID):
    return db.session.get(RFP, (groupID, lotID))

def get_all_rfps():
    return db.session.scalars(
        db.select(RFP)
    ).all()

def get_all_rfps_json():
    rfps = get_all_rfps()
    if not rfps:
        return []
    rfps = [rfp.get_json() for rfp in rfps]
    return rfps

def remove_rfp(groupID, lotID):
    rfp = get_rfp(groupID, lotID)
    if rfp:
        bids = db.session.scalars(
            db.select(Bid)
            .filter_by(lotID= lotID)
        )

        for bid in bids:
            remove_bid(bid.id)

        db.session.delete(rfp)
        db.session.commit()
        return True
    return False
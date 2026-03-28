from App.models import Bid
from App.database import db

def create_bid(lotID, sourceGroupID, receipientGroupID, bidDocumentLink):
    newbid = Bid(lotID, sourceGroupID, receipientGroupID, bidDocumentLink)
    db.session.add(newbid)
    db.session.commit()
    return newbid

def get_bid(id):
    return db.session.get(Bid, id)

def get_all_bids():
    return db.session.scalars(db.select(Bid)).all()

def get_all_bids_json():
    bids = get_all_bids()
    if not bids:
        return []
    bids = [bid.get_json() for bid in bids]
    return bids

def remove_bid(id):
    bid = get_bid(id)
    if bid:
        db.session.delete(bid)
        db.session.commit()
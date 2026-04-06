from App.models import LotGroup, RFP, Bid, Evaluation, Group
from App.database import db
from sqlalchemy import and_, or_
from .rfp import remove_rfp
from .bid import remove_bid
from .evaluation import remove_evaluation

def add_lotGroup(lotID, groupID):
    newentry = LotGroup(lotID, groupID)
    db.session.add(newentry)
    db.session.commit()

def get_lotGroup(lotID, groupID):
    return db.session.get(LotGroup, (lotID, groupID))

def get_all_lotGroups():
    return db.session.scalars(
        db.select(LotGroup)
    ).all()

def get_all_lotGroups_json():
    entries = get_all_lotGroups()
    if not entries:
        return []
    entries = [entry.get_json() for entry in entries]
    return entries

def remove_lotGroup(lotID, groupID):
    entry = get_lotGroup(lotID, groupID)
    if entry:
        nextLot = db.session.scalars(
            db.select(LotGroup)
            .filter(and_(LotGroup.groupID == groupID, LotGroup.lotID != lotID))
        ).first()

        group = db.session.scalars(
            db.select(Group)
            .filter_by(id=groupID)
        ).first()

        group.status = "pending"

        rfps = db.session.scalars(
            db.select(RFP)
            .filter(or_(RFP.lotID == lotID, RFP.groupID == groupID))
        ).all()

        for rfp in rfps:
            remove_rfp(rfp.groupID, rfp.lotID)

        bids = db.session.scalars(
            db.select(Bid)
            .filter(or_(Bid.lotID == lotID, Bid.sourceGroupID == groupID, Bid.recipientGroupID == groupID))
        ).all()

        for bid in bids:
            remove_bid(bid.id)

        evals = db.session.scalars(
            db.select(Evaluation)
            .filter(or_(Evaluation.sourceGroupID == groupID, Evaluation.recipientGroupID == groupID, Evaluation.lotID == lotID))
        ).all()

        for eva in evals:
            remove_evaluation(eva.id)

        db.session.delete(entry)
        db.session.commit()
        return True
    return False
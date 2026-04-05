from App.models import *
from .bid import remove_bid
from .evaluation import remove_evaluation
from .rfp import remove_rfp
from .studentGroup import remove_studentGroup
from .lotGroup import remove_lotGroup
from App.database import db
from sqlalchemy import or_

def create_group(groupName):
    group = Group(groupName)
    db.session.add(group)
    db.session.flush()
    group.set_generated_name()
    db.session.commit()
    return group

def approve_group(id):
    group = get_group(id)
    group.status = "approved"
    db.session.commit()

def get_group(id):
    return db.session.get(Group, id)

def get_all_groups():
    return db.session.scalars(
        db.select(Group)
    ).all()

def get_all_groups_json():
    groups = get_all_groups()
    if not groups:
        return []
    groups = [group.get_json() for group in groups]
    return groups

def remove_group(id):
    group = get_group(id)
    if group:
        entries = db.session.scalars(
            db.select(Bid)
            .filter(or_(Bid.sourceGroupID == id, Bid.recipientGroupID == id))
        ).all()

        for entry in entries:
            removed = remove_bid(entry.id)

        entries = db.session.scalars(
            db.select(Evaluation)
            .filter(or_(Evaluation.sourceGroupID == id, Evaluation.recipientGroupID == id))
        ).all()

        for entry in entries:
            removed = remove_evaluation(entry.id)

        entries = db.session.scalars(
            db.select(RFP)
            .filter_by(groupID = id)
        ).all()

        for entry in entries:
            removed = remove_rfp(id, entry.lotID)

        entries = db.session.scalars(
            db.select(StudentGroup)
            .filter_by(groupID = id)
        ).all()

        for entry in entries:
            removed = remove_studentGroup(entry.studentID, id)

        entries = db.session.scalars(
            db.select(LotGroup)
            .filter_by(groupID = id)
        ).all()

        for entry in entries:
            removed = remove_lotGroup(entry.lotID, id)
        
        db.session.delete(group)
        db.session.commit()
        return True
    return False
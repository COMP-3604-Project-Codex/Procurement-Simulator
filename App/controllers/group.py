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
        members = db.session.scalars(
            db.select(StudentGroup)
            .filter_by(groupID=id)
        ).all()

        for member in members:
            remove_studentGroup(member.studentID, member.groupID)

        lotGroups = db.session.scalars(
            db.select(LotGroup)
            .filter_by(groupID=id)
        ).all()

        for lotGroup in lotGroups:
            remove_lotGroup(lotGroup.lotID, lotGroup.groupID)
        
        db.session.delete(group)
        db.session.commit()
        return True
    return False
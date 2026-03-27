from App.models import GroupRequest
from App.database import db

def create_groupRequest(groupName, members):
    duplicates = []

    for member in members:
        existing = db.session.scalars(db.select(GroupRequest).filter(GroupRequest.members.contains(member))).first()
        if existing:
            duplicates.append(member)

    if not duplicates:
        newreq = GroupRequest(groupName, members)
        db.session.add(newreq)
        db.session.commit()
        return {
            "id": newreq.id,
            "status": "good",
            "message": "GroupRequest was sent successfully",
            "duplicates": duplicates
        }
    else:
        return {
            "id": 0,
            "status": "bad",
            "message": "You or a member you are trying to add is already in a group request",
            "duplicates": duplicates
        }

def get_groupRequest(id):
    return db.session.get(GroupRequest, id)

def get_all_groupRequests():
    return db.session.scalars(db.select(GroupRequest)).all()

def get_all_groupRequests_json():
    reqs = get_all_groupRequests()
    if not reqs:
        return []
    reqs = [req.get_json() for req in reqs]
    return reqs

def remove_groupRequest(id):
    req = get_groupRequest(id)
    if req:
        db.session.delete(req)
        db.session.commit()
        return True
    return False
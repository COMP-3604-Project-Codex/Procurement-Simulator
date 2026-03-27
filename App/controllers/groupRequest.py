from App.models import GroupRequest
from App.database import db

def create_groupRequest(groupName, members):
    newreq = GroupRequest(groupName, members)
    db.session.add(newreq)
    db.session.commit()

def get_groupRequest(id):
    return db.session.get(GroupRequest, id)

def get_all_groupRequest():
    return db.session.scalars(db.select(GroupRequest)).all()

def get_all_groupRequest_json():
    reqs = get_all_groupRequest()
    if not reqs:
        return []
    reqs = [req.get_json() for req in reqs]
    return reqs

def remove_groupRequest(id):
    req = get_groupRequest(id)
    if req:
        db.session.delete(req)
        db.session.commit()
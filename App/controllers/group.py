from App.models import Group
from App.database import db

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
    return db.session.scalars(db.select(Group)).all()

def get_all_groups_json():
    groups = get_all_groups()
    if not groups:
        return []
    groups = [group.get_json() for group in groups]
    return groups

def remove_group(id):
    group = get_group(id)
    if group:
        db.session.delete(group)
        db.session.commit()
        return True
    return False
from App.models import LotGroup
from App.database import db

def add_lotGroup(lotID, groupID):
    newentry = LotGroup(lotID, groupID)
    db.session.add(newentry)
    db.session.commit()

def get_lotGroup(lotID, groupID):
    return db.session.get(LotGroup, (lotID, groupID))

def get_all_lotGroups():
    return db.session.scalars(db.select(LotGroup)).all()

def get_all_lotGroups_json():
    entries = get_all_lotGroups()
    if not entries:
        return []
    entries = [entry.get_json() for entry in entries]
    return entries

def remove_lotGroup(lotID, groupID):
    entry = get_lotGroup(lotID, groupID)
    if entry:
        db.session.delete(entry)
        db.session.commit()
        return True
    return False
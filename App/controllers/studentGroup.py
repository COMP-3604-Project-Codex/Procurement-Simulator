from App.models import StudentGroup
from App.database import db

def add_studentGroup(studentID, groupID):
    newentry = StudentGroup(studentID, groupID)
    db.session.add(newentry)
    db.session.commit()

def get_studentGroup(studentID, groupID):
    return db.session.get(StudentGroup, (studentID, groupID))

def get_all_studentGroups():
    return db.session.scalars(db.select(StudentGroup)).all()

def get_all_studentGroups_json():
    entries = get_all_studentGroups()
    if not entries:
        return []
    entries = [entry.get_json() for entry in entries]
    return entries

def remove_studentGroup(studentID, groupID):
    entry = get_studentGroup(studentID, groupID)
    if entry:
        db.session.delete(entry)
        db.session.commit()
        return True
    return False
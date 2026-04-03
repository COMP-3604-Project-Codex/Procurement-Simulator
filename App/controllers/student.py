from App.models import Student
from App.database import db

def create_student(name, username, password):
    newstudent = Student(name=name, username=username, password=password)
    db.session.add(newstudent)
    db.session.commit()

def get_student(id):
    return db.session.get(Student, id)

def get_all_students():
    return db.session.scalars(db.select(Student)).all()

def get_all_students_json():
    students = get_all_students()
    if not students:
        return []
    students = [student.get_json() for student in students]
    return students
from .user import create_user
from App.database import db
from .lot import create_lot
from .student import create_student
from .admin import create_admin

def initialize():
    db.drop_all()
    db.create_all()
    
    create_admin("bob", "bobpass")

    create_lot("GIS Lab", "Medium, capable of having 20 machines", 160000.00)
    create_lot("Government Office Lab", "Medium, capable of having 20 machines", 110000.00)
    create_lot("University Computer Lab", "Medium, capable of having 20 machines", 250000.00)
    create_lot("Data Center", "Medium, capable of having 20 machines", 25000000.00)

    create_student("jack", "jackpass")
    create_student("cooper", "cooperpass")
    create_student("john", "johnpass")
    create_student("tony", "tonypass")

    create_student("peper", "peperpass")
    create_student("steve", "stevepass")
    create_student("clint", "clintpass")
    create_student("bruce", "brucepass")

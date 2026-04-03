from .user import create_user
from App.database import db
from .lot import create_lot
from .student import create_student
from .admin import create_admin
from App.models import *

def initialize():
    db.drop_all()
    db.create_all()
    
    create_admin("bob", "bobpass")

    create_lot("GIS Lab", "Medium, capable of having 20 machines", 160000.00)
    create_lot("Government Office Lab", "Medium, capable of having 20 machines", 110000.00)
    create_lot("University Computer Lab", "Medium, capable of having 20 machines", 250000.00)
    create_lot("Data Center", "Medium, capable of having 20 machines", 25000000.00)

    create_student("jack", "20240123", "jackpass")
    create_student("cooper", "20231245", "cooperpass")
    create_student("john", "20229876", "johnpass")
    create_student("tony", "20235678", "tonypass")

    create_student("peper", "20246789", "peperpass")
    create_student("steve", "20242345", "stevepass")
    create_student("clint", "20238901", "clintpass")
    create_student("bruce", "20238902", "brucepass")

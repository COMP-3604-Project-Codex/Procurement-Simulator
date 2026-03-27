from App.models import Lot
from App.database import db

def create_lot(labType, labSize, budget):
    newlot = Lot(labType, labSize, budget)
    db.session.add(newlot)
    db.session.flush()
    newlot.set_generated_name()
    db.session.commit()

def get_lot(id):
    return db.session.get(Lot, id)

def get_all_lots():
    return db.session.scalars(db.select(Lot)).all()

def get_all_lots_json():
    lots = get_all_lots()
    if not lots:
        return []
    lots = [lot.get_json() for lot in lots]
    return lots

def edit_lot(id, labType=None, labSize=None, budget=None):
    lot = get_lot(id)
    if lot:
        if labType:
            lot.labType = labType

        if labSize:
            lot.labSize = labSize
        
        if budget:
            lot.budget = budget
        
        db.session.commit()

def remove_lot(id):
    lot = get_lot(id)
    if lot:
        db.session.delete(lot)
        db.session.commit()
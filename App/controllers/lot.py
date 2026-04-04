from App.models import Lot
from App.database import db
from sqlalchemy.orm.attributes import flag_modified

def create_lot(labType, labSize, budget):
    newlot = Lot(labType, labSize, budget)
    db.session.add(newlot)
    db.session.flush()
    newlot.set_generated_name()
    db.session.commit()

def get_lot(id):
    return db.session.get(Lot, id)

def get_all_lots():
    return db.session.scalars(
        db.select(Lot)
    ).all()

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

def edit_lotRFP_details(id, deviceType=None, resolution=None, os=None, cpu=None, ram=None, drive=None, gpu=None, peripherals=None, features=None, io=None):
    lot = get_lot(id)
    if lot:
        if deviceType is not None:
            lot.deviceType = deviceType
        if resolution is not None:
            lot.resolution = resolution
        if os is not None:
            lot.os = os
        if cpu is not None:
            lot.cpu = cpu
        if ram is not None:
            lot.ram = ram
        if drive is not None:
            lot.drive = drive
        if gpu is not None:
            lot.gpu = gpu
        if peripherals is not None:
            lot.peripherals = peripherals
        if features is not None:
            lot.features = features
        if io is not None:
            lot.io = io

        db.session.commit()
        return lot
    return None

def get_lotRFP_details_json(id):
    lot = get_lot(id)
    if lot:
        return lot.specs
    return None

def remove_lot(id):
    lot = get_lot(id)
    if lot:
        db.session.delete(lot)
        db.session.commit()
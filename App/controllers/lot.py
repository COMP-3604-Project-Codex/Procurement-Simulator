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

def edit_lotRFP_details(id, deviceType=None, resolution=None, os=None, cpu=None, ram=None, drive=None, gpu=None, peripherals=None, features=None, io=None):
    lot = get_lot(id)
    if lot:
        if deviceType:
            lot.deviceType = deviceType
        if resolution:
            lot.resolution = resolution
        if os:
            lot.os = os
        if cpu:
            lot.cpu = cpu
        if ram:
            lot.ram = ram
        if drive:
            lot.drive = drive
        if gpu:
            lot.gpu = gpu
        if peripherals:
            lot.peripherals = peripherals
        if features:
            lot.features = features
        if io:
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
from App.models import Evaluation
from App.database import db

def create_evaluation(sourceGroupID, receipientGroupID, bidID, lotID, specsMet, presentation, professionalism, budget):
    neweval = Evaluation(sourceGroupID, receipientGroupID, bidID, lotID, specsMet, presentation, professionalism, budget)
    db.session.add(neweval)
    db.session.commit()
    return neweval

def edit_evaluation(id, specsMet, presentation, professionalism, budget, deviceType=None, resolution=None, os=None, cpu=None, ram=None, drive=None, gpu=None, peripherals=None, features=None, io=None):
    eva = get_evaluation(id)
    if eva:
        eva.overallScore = round((((specsMet + presentation + professionalism + budget)/25) * 10), 1)

        if deviceType:
            eva.deviceType = deviceType
        if resolution:
            eva.resolution = resolution
        if os:
            eva.os = os
        if cpu:
            eva.cpu = cpu
        if ram:
            eva.ram = ram
        if drive:
            eva.drive = drive
        if gpu:
            eva.gpu = gpu
        if peripherals:
            eva.peripherals = peripherals
        if features:
            eva.features = features
        if io:
            eva.io = io

        db.session.commit()
        return True
    return False

def select_evaluation(id):
    evaluation = get_evaluation(id)
    evaluation.status = "selected"
    db.session.commit()

def get_evaluation(id):
    return db.session.get(Evaluation, id)

def get_all_evaluations():
    return db.session.scalars(db.select(Evaluation)).all()

def get_all_evaluations_json():
    evals = get_all_evaluations()
    if not evals:
        return []
    evals = [eva.get_json() for eva in evals]
    return evals

def remove_evaluation(id):
    eva = get_evaluation(id)
    if eva:
        db.session.delete(eva)
        db.session.commit()
        return True
    return False
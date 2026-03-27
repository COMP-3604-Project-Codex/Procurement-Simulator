from App.database import db

class Lot(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(10))
    labType = db.Column(db.String(30), nullable=False)
    labSize = db.Column(db.Integer, nullable=False)
    budget = db.Column(db.Float, nullable=False)
    specs = db.Column(db.JSON)

    def __init__(self, labType, labSize, budget):
        self.labType = labType
        self.labSize = labSize
        self.budget = budget
        self.specs = {
            "deviceType": "",
            "resolution": "",
            "os": "",
            "cpu": "",
            "ram": "",
            "drive": "",
            "gpu": "",
            "peripherals": "",
            "features": "",
            "io": "" 
        }

    def set_generated_name(self):
        self.name = f"Lot {self.id}"

    def get_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'labType': self.labType,
            'labSize': self.labSize,
            'budget': self.budget
        }
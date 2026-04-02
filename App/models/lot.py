from App.database import db

class Lot(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(10))
    labType = db.Column(db.String(30), nullable=False)
    labSize = db.Column(db.Integer, nullable=False)
    budget = db.Column(db.Float, nullable=False)
    deviceType = db.Column(db.String(1000), default="")
    resolution = db.Column(db.String(1000), default="")
    os = db.Column(db.String(1000), default="")
    cpu = db.Column(db.String(1000), default="")
    ram = db.Column(db.String(1000), default="")
    drive = db.Column(db.String(1000), default="")
    gpu = db.Column(db.String(1000), default="")
    peripherals = db.Column(db.String(1000), default="")
    features = db.Column(db.String(1000), default="")
    io = db.Column(db.String(1000), default="")

    def __init__(self, labType, labSize, budget):
        self.labType = labType
        self.labSize = labSize
        self.budget = budget

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
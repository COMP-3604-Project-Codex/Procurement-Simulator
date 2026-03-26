from App.database import db

class Lot(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    labType = db.Column(db.String(30), nullable=False)
    labSize = db.Column(db.Integer, nullable=False)
    budget = db.Column(db.Float, nullable=False)

    def __init__(self, labType, labSize, budget):
        self.labType = labType
        self.labSize = labSize
        self.budget = budget

    def get_json(self):
        return {
            'id': self.id,
            'labType': self.labType,
            'labSize': self.labSize,
            'budget': self.budget
        }
from App.database import db

class RFPRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    groupID = db.Column(db.Integer, db.ForeignKey('group.id'), nullable=False)
    lotID = db.Column(db.Integer, db.ForeignKey('lot.id'), nullable=False)
    specs = db.Column(db.JSON)

    def __init__(self, groupID, lotID, specs):
        self.groupID = groupID
        self.lotID = lotID
        self.specs = specs

    def get_json(self):
        return {
            'id': self.id,
            'groupID': self.groupID,
            'lotID': self.lotID,
            'specs': self.specs
        }
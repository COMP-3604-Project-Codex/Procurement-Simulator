from App.database import db

class RFPRequest(db.Model):
    groupID = db.Column(db.Integer, db.ForeignKey('group.id'), primary_key=True)
    lotID = db.Column(db.Integer, db.ForeignKey('lot.id'), primary_key=True)
    specs = db.Column(db.JSON)

    def __init__(self, groupID, lotID, specs):
        self.groupID = groupID
        self.lotID = lotID
        self.specs = specs

    def get_json(self):
        return {
            'groupID': self.groupID,
            'lotID': self.lotID,
            'specs': self.specs
        }
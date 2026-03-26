from App.database import db

class Evaluation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sourceGroupID = db.Column(db.Integer, db.ForeignKey('group.id'), nullable=False)
    receipientGroupID = db.Column(db.Integer, db.ForeignKey('group.id'), nullable=False)
    evaluationDetails = db.Column(db.JSON)

    def __init__(self, sourceGroupID, receipientGroupID, evaluationDetails):
        self.sourceGroupID = sourceGroupID
        self.receipientGroupID = receipientGroupID
        self.evaluationDetails = evaluationDetails

    def get_json(self):
        return {
            'id': self.id,
            'sourceGroupID': self.sourceGroupID,
            'receipientGroupID': self.receipientGroupID,
            'evaluationDetails': self.evaluationDetails
        }
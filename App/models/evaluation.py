from App.database import db

class Evaluation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sourceGroupID = db.Column(db.Integer, db.ForeignKey('group.id'), nullable=False)
    receipientGroupID = db.Column(db.Integer, db.ForeignKey('group.id'), nullable=False)
    bidID = db.Column(db.Integer, db.ForeignKey('bid.id'), nullable=False)
    lotID = db.Column(db.Integer, db.ForeignKey('lot.id'), nullable=False)
    status = db.Column(db.String(30), default="draft")
    overallScore = db.Column(db.Float, default=0.0)
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

    def __init__(self, sourceGroupID, receipientGroupID, bidID, lotID, specsMet, presentation, professionalism, budget):
        self.bidID = bidID
        self.lotID = lotID
        self.sourceGroupID = sourceGroupID
        self.receipientGroupID = receipientGroupID
        self.overallScore = round((((specsMet + presentation + professionalism + budget)/25) * 10), 1)

    def get_json(self):
        return {
            'id': self.id,
            'sourceGroupID': self.sourceGroupID,
            'receipientGroupID': self.receipientGroupID,
            'bidID': self.bidID,
            'lotID': self.lotID,
            'overallScore': self.overallScore
        }
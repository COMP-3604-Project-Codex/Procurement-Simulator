from App.database import db
from datetime import datetime

class Bid(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    lotID = db.Column(db.Integer, db.ForeignKey('lot.id'), nullable=False)
    sourceGroupID = db.Column(db.Integer, db.ForeignKey('group.id'), nullable=False)
    receipientGroupID = db.Column(db.Integer, db.ForeignKey('group.id'), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.now)
    bidDocument = db.Column(db.LargeBinary, nullable=False)
    bidDocumentName = db.Column(db.String(255), nullable=False)  # to store the original filename

    def __init__(self, lotID, sourceGroupID, receipientGroupID, bidDocument, bidDocumentName):
        self.lotID = lotID
        self.sourceGroupID = sourceGroupID
        self.receipientGroupID = receipientGroupID
        self.bidDocument = bidDocument
        self.bidDocumentName = bidDocumentName
        self.timestamp = datetime.now()

    def get_json(self):
        return {
            'id': self.id,
            'lotID': self.lotID,
            'sourceGroupID': self.sourceGroupID,
            'receipientGroupID': self.receipientGroupID,
            'timestamp': self.timestamp.isoformat(),
            'bidDocumentName': self.bidDocumentName
        }
from App.database import db
from datetime import datetime

class Bid(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    lotID = db.Column(db.Integer, db.ForeignKey('lot.id'), nullable=False)
    sourceGroupID = db.Column(db.Integer, db.ForeignKey('group.id'), nullable=False)
    receipientGroupID = db.Column(db.Integer, db.ForeignKey('group.id'), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    bidDocumentlink = db.Column(db.String(100), nullable=False)

    def __init__(self, lotID, sourceGroupID, receipientGroupID, bidDocumentlink):
        self.lotID = lotID
        self.sourceGroupID = sourceGroupID
        self.receipientGroupID = receipientGroupID
        self.bidDocumentlink = bidDocumentlink

    def get_json(self):
        return {
            'id': self.id,
            'lotID': self.lotID,
            'sourceGroupID': self.sourceGroupID,
            'receipientGroupID': self.receipientGroupID,
            'timestamp': self.timestamp.isoformat(),
            'bidDocumentlink': self.bidDocumentlink
        }
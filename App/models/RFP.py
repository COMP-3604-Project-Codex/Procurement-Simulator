from App.database import db

class RFP(db.Model):
    groupID = db.Column(db.Integer, db.ForeignKey('group.id'), primary_key=True)
    lotID = db.Column(db.Integer, db.ForeignKey('lot.id'), primary_key=True)
    status = db.Column(db.String(30), default="requested")
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

    def __init__(self, groupID, lotID):
        self.groupID = groupID
        self.lotID = lotID

    def get_json(self):
        return {
            'groupID': self.groupID,
            'lotID': self.lotID,
            'status': self.status,
            'Type': self.deviceType,
            'Screen Size & Resolution': self.resolution,
            'Operating System(s)': self.os,
            'CPU': self.cpu,
            'Memory (RAM)': self.ram,
            'Hard Drive': self.drive,
            'Graphics': self.gpu,
            'External Peripherals': self.peripherals,
            'Features': self.features,
            'I/O': self.io
        }
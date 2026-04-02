from App.database import db

class Group(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    groupName = db.Column(db.String(30), nullable=False, unique=True)
    status = db.Column(db.String(30), nullable=False, default="requested")

    def __init__(self, groupName):
        self.groupName = groupName

    def set_generated_name(self):
        self.groupName = f"G{self.id} {self.groupName}"

    def get_json(self):
        return {
            'id': self.id,
            'groupName': self.groupName,
            'status': self.status
        }
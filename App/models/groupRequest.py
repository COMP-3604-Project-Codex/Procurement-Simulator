from App.database import db
from sqlalchemy.dialects.postgresql import ARRAY

class GroupRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    groupName = db.Column(db.String(30), nullable=False, unique=True)
    members = db.Column(ARRAY(db.Integer), nullable=False, default=[])

    def __init__(self, groupName, members: list[int]):
        self.groupName = groupName
        self.members = members

    def get_json(self):
        return {
            'id': self.id,
            'groupName': self.groupName,
            'members': self.members
        }
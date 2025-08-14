from myBlueprints import db
from datetime import datetime
class ChatMessages(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    sender = db.Column(db.String(100),nullable=False)
    receiver = db.Column(db.String(100),nullable=False)
    message = db.Column(db.String(50),nullable=False)
    timestamp = db.Column(db.DateTime,default=datetime.utcnow)
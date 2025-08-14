from myBlueprints import db
from datetime import datetime

class ChatbotMessages(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    user_message = db.Column(db.String,nullable=False)
    bot_message = db.Column(db.String,nullable=False)
    user_id = db.Column(db.String(100),nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
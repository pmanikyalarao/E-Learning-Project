from myBlueprints import db
class ChatFriends(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(100),nullable=False)
    friend_username = db.Column(db.String(100),nullable=False)
    notifications = db.Column(db.Integer,default=0)
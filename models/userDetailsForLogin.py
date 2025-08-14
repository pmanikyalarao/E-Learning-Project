from myBlueprints import db
class UserDetails(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(100),nullable=False)
    email = db.Column(db.String(100),nullable=False,unique=True)
    password = db.Column(db.String(50),nullable=False)
    phone = db.Column(db.Integer,nullable=False)
    username = db.Column(db.String(100),nullable=False,unique=True)
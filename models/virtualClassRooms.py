from myBlueprints import db
from datetime import datetime


class VirtualClasses(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    faculty_username = db.Column(db.String(100),nullable=False)
    class_name = db.Column(db.String(100),nullable=False)
    class_id = db.Column(db.String(50),nullable=False,unique=True)
    no_of_students_joined = db.Column(db.Integer,default=0)
    
class StudentsJoined(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    student_username = db.Column(db.String(100),nullable=False)
    faculty_username = db.Column(db.String(100),nullable=False)
    class_name = db.Column(db.String(100),nullable=False)
    class_id = db.Column(db.String(50),nullable=False)


class ClassFiles(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    faculty_username = db.Column(db.String(100), nullable=False)
    class_name = db.Column(db.String(100), nullable=False)
    class_id = db.Column(db.Integer, nullable=False)
    file_name = db.Column(db.String(200), nullable=False)
    file_type = db.Column(db.String(50), nullable=False)
    file = db.Column(db.LargeBinary, nullable=False)
    timestamp = db.Column(db.DateTime,default=datetime.utcnow)

class GroupChatMessages(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender = db.Column(db.String(100), nullable=False)
    class_id = db.Column(db.String(100), nullable=False)  # Use class_id instead of room
    message = db.Column(db.String(500), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    
# Database model for recorded classes
# class RecordedClass(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     class_id = db.Column(db.String(100), nullable=False)
#     video_data = db.Column(db.LargeBinary, nullable=False)  # Store recorded stream as binary data
#     timestamp = db.Column(db.DateTime, default=datetime.utcnow)

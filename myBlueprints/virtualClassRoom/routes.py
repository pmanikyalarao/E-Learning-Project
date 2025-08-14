from flask import request,render_template,flash,redirect,url_for,Blueprint,session,jsonify,send_file
from flask_socketio import SocketIO,emit
from io import BytesIO
from random import random
import string
from random import choice
from models.virtualClassRooms import VirtualClasses,StudentsJoined,ClassFiles,GroupChatMessages
from ..extensions import db,socketio

virtualClassRoom_pg = Blueprint("virtualClassRoom_pg",
                                __name__,
                                template_folder="templates",
                                static_folder="virtualClassStatic")


# To store active students per class
class_active_students = {}
# Store connected students in the form {class_id: [sids]}
current_connected_students = {}

def generateClassId():
    characters = string.ascii_letters + string.digits + '_'
    return "".join(choice(characters) for _ in range(16))

@virtualClassRoom_pg.route("/virtualClassRoom")
def virtualClassPage():
    facultyClasses = VirtualClasses.query.filter_by(faculty_username = session.get('username')).all()
    joinedClasses = StudentsJoined.query.filter_by(student_username = session.get('username')).all()
    return render_template("virtualClass.html",facultyClasses=facultyClasses,joinedClasses=joinedClasses)

@virtualClassRoom_pg.route("/createVirtualClass",methods = ["GET","POST"])
def createClass():
    className = request.form.get('className')
    facultyUsername = session.get('username')
    classId = generateClassId()
    if(VirtualClasses.query.filter((VirtualClasses.class_name == className) & (VirtualClasses.faculty_username == session.get("username"))).all()):
        return {'text':'classAlreadyExisting'}
    while True:
        if(VirtualClasses.query.filter(VirtualClasses.class_id == classId).all()):
            classId = generateClassId()
        else:
            break
    myClass = VirtualClasses(faculty_username=facultyUsername,class_name=className,class_id=classId)
    db.session.add(myClass)
    db.session.commit()
    return {'text':'created','id':classId}

@virtualClassRoom_pg.route("/checkVirtualClass",methods = ["GET","POST"])
def checkClass():
    classId = request.form.get('classId')
    find = VirtualClasses.query.filter(VirtualClasses.class_id == classId).first()
    if find:
        return {"text":"existing","className":find.class_name,"classId":find.class_id,"facultyUsername":find.faculty_username}
    else:
        return {"text":"notExisting"}
    
@virtualClassRoom_pg.route("/joinVirtualClass",methods = ["GET","POST"])
def joinClass():
    classId = request.form.get('classId')
    find = VirtualClasses.query.filter(VirtualClasses.class_id == classId).first()
    if find:
        if StudentsJoined.query.filter((StudentsJoined.student_username == session.get("username")) & (StudentsJoined.class_id == classId)).first():
            return {"text":"alreadyJoined"}
        stu = StudentsJoined(student_username=session.get("username"),faculty_username=find.faculty_username,class_name=find.class_name,class_id=classId)
    
        find.no_of_students_joined += 1
    
        db.session.add(stu)
        db.session.commit()
    
        return {"text":"joined","className":stu.class_name,"classId":stu.class_id,"facultyUsername":stu.faculty_username}
    else:
        return {"text":"notJoined"}
    


#implementation of virtual clasess
@virtualClassRoom_pg.route('/facultyClass/<classId>')
def facultyClass(classId):
    return render_template("facultyClass.html",classId = classId)

@virtualClassRoom_pg.route('/studentClass/<classId>')
def studentClass(classId):
    return render_template("studentClass.html",classId = classId)






#Faculty Upload File
@virtualClassRoom_pg.route('/faculty/upload/<class_id>', methods=['GET','POST'])
def faculty_upload(class_id):
    myClass = VirtualClasses.query.filter(VirtualClasses.class_id == class_id).first()
    faculty_username = myClass.faculty_username
    class_name = myClass.class_name
    # class_id = myClass.class_id

        

    # Handle file upload
    file = request.files['file']
    if file:
        file_name = file.filename
        file_type = file.content_type
        # file_path = os.path.join(app.config['UPLOAD_FOLDER'], file_name)
        # file.save(file_path)

        # Store in DB
        new_file = ClassFiles(
            faculty_username=faculty_username,
            class_name=class_name,
            class_id=class_id,
            file_name=file_name,
            file_type=file_type,
            file=file.read()
        )
        db.session.add(new_file)
        db.session.commit()

        # Broadcast to students
        if class_id in class_active_students:
            for sid in class_active_students[class_id]:
                # if(sid == request.sid):
                #     continue
                # else:
                socketio.emit('file_shared', {
                    'file_name': file_name,
                    'file_type': file_type,
                    'faculty_username': faculty_username,
                    'class_name': class_name
                }, room=sid)

        return jsonify({'message': 'uploaded','faculty_username':new_file.faculty_username,'file_name':new_file.file_name})
    return jsonify({'message': 'No file uploaded!'})

#Student File Sharing Access
@virtualClassRoom_pg.route('/class/<class_id>/file_history', methods=['GET'])
def get_file_history(class_id):
    files = ClassFiles.query.filter_by(class_id=class_id).order_by(ClassFiles.timestamp.asc()).all()
    file_list = []
    for file in files:
        file_list.append({
            'file_name': file.file_name,
            'file_type': file.file_type,
            'faculty_username': file.faculty_username,
            'class_name': file.class_name
        })
    return jsonify(file_list)

#Download File Route
@virtualClassRoom_pg.route('/student/download/<filename>', methods=['GET'])
def download_file(filename):
    file_data = ClassFiles.query.filter_by(file_name=filename).first()
    return send_file(BytesIO(file_data.file), download_name=file_data.file_name, mimetype=file_data.file_type)


#Student Accessing File Sharing
@socketio.on('student_access_file_sharing')
def student_access_file_sharing(data):
    class_id = data['class_id']
    sid = request.sid

    if class_id not in class_active_students:
        class_active_students[class_id] = []

    if sid not in class_active_students[class_id]:
        class_active_students[class_id].append(sid)

#Remove Student on Disconnect
@socketio.on('disconnect')
def on_disconnect():
    sid = request.sid
    for class_id, sids in class_active_students.items():
        if sid in sids:
            sids.remove(sid)
            break
    # for class_id, value in current_connected_students.items():
    #     for sids in current_connected_students[class_id]['students']:
    #         if sid == sids:
    #             current_connected_students[class_id]['students'].remove(sid)
    #             break


# API to fetch chat history for a specific class_id
@virtualClassRoom_pg.route('/class/<class_id>/messages')
def get_messages(class_id):
    messages = GroupChatMessages.query.filter_by(class_id=class_id).order_by(GroupChatMessages.timestamp).all()
    messages_list = []
    myClass = VirtualClasses.query.filter(VirtualClasses.class_id == class_id).first()
    for message in messages:
        if(message.sender == myClass.faculty_username):
            faculty = "true"
        else:
            faculty = "false"
        messages_list.append({
            'sender': message.sender,
            'message': message.message,
            'faculty': faculty
        })
    return jsonify(messages_list)

# SocketIO event: Handle messages sent to the class chat
@socketio.on('message')
def handle_message(data):
    class_id = data['class_id']
    message = data['message']
    sender = data['sender']
    

    # Store the message in the database
    new_message = GroupChatMessages(sender=sender, class_id=class_id, message=message)
    db.session.add(new_message)
    db.session.commit()
    
    myClass = VirtualClasses.query.filter(VirtualClasses.class_id == class_id).first()
    if(sender == myClass.faculty_username):
        faculty = "true"
    else:
        faculty = "false"
    # Broadcast message to the class chat
    if class_id in class_active_students:
        for sid in class_active_students[class_id]:
            if(sid == request.sid):
                continue
            else:
                emit('message',{'sender': sender, 'message': message, 'faculty': faculty}, room=sid)
                
                
                
                
#for Live streaming
@socketio.on('joinCurrentConnectedStudents')
def handle_joinCurrentConnectedStudents(data):
    class_id = data['class_id']
    if class_id in current_connected_students:
        if request.sid in class_active_students[class_id]:
            emit('faculty_stream', room=request.sid)

@socketio.on('join_class')
def join_class(data):
    class_id = data['class_id']
    sid = request.sid
    if class_id in current_connected_students:
        current_connected_students[class_id]['students'].append(sid)
        emit('stream_started',current_connected_students[class_id]['url'],room=sid)
    # print(f"Student {sid} joined class {class_id}")

@socketio.on('leave_class')
def leave_class(data):
    class_id = data['class_id']
    sid = request.sid
    if class_id in current_connected_students and sid in current_connected_students[class_id]['students']:
        current_connected_students[class_id]['students'].remove(sid)
        # print(f"Student {sid} left class {class_id}")

@socketio.on('start_stream')
def start_stream(data):
    class_id = data['class_id']
    stream_url = data['stream_url']
    if class_id not in current_connected_students:
        current_connected_students[class_id] = {"url":stream_url,"students":[]}
    if class_id in class_active_students:
        for sid in class_active_students[class_id]:
            emit('faculty_stream', room=sid)
        # print(f"Streaming started for class {class_id}")

@socketio.on('stop_stream')
def stop_stream(data):
    class_id = data['class_id']
    if class_id in current_connected_students:
        emit('stream_stopped', room=current_connected_students[class_id]['students'])
        del current_connected_students[class_id]
        # print(f"Streaming stopped for class {class_id}")
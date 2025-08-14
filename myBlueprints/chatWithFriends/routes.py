from flask import Blueprint,url_for,redirect,render_template,session,jsonify,request
from ..extensions import socketio
from flask_socketio import SocketIO,emit
from models.chatAppFriendsList import ChatFriends
from models.chatAppMessages import ChatMessages
from models.userDetailsForLogin import UserDetails
from ..extensions import db

connectedUsers = {}

chatWithFriends_pg = Blueprint("chatWithFriends_pg",
                               __name__,
                                template_folder="templates",
                                static_folder="chatWithFriendsStatic")


@chatWithFriends_pg.route("/chatWithFriends")
def chatWithFriendsWebPage():
    friends = ChatFriends.query.filter((ChatFriends.username == session.get('username'))).order_by(ChatFriends.friend_username.asc()).all()
    return render_template("chatApp.html",friends = friends)

@chatWithFriends_pg.route('/searchFriend/<friend_id>',methods=['GET','POST'])
def searchFriend(friend_id):
    checkUser = UserDetails.query.filter_by(username = friend_id).first()
    if(checkUser):
        checkAdded = ChatFriends.query.filter((ChatFriends.username == session.get('username')) & (ChatFriends.friend_username == friend_id)).first()
        if(checkAdded):
            return {'data':'found','check':'added'}
        else:
            return {'data':'found','check':'notAdded'}
            
    else:
        return {'data':'notFound'}

@chatWithFriends_pg.route('/addFriend/<friend_id>',methods=['GET','POST'])
def addFriend(friend_id):
    checkAdded1 = ChatFriends.query.filter((ChatFriends.username == session.get('username')) & (ChatFriends.friend_username == friend_id)).first()
    checkAdded2 = ChatFriends.query.filter((ChatFriends.username == friend_id) & (ChatFriends.friend_username == session.get('username'))).first()
    if((not checkAdded2) and (not checkAdded2)):
        if(friend_id == session.get('username')):
            friend = ChatFriends(username = session.get('username'),friend_username = friend_id)
            db.session.add(friend) 
        else:
            friend1 = ChatFriends(username = session.get('username'),friend_username = friend_id)
            friend2 = ChatFriends(username = friend_id,friend_username = session.get('username'))
            db.session.add(friend1)
            db.session.add(friend2)
        db.session.commit()
    return 'true'

@chatWithFriends_pg.route('/load_messages/<friend_id>',methods=['GET',"POST"])
def load_messages(friend_id):
    user_id = session.get('username')
    # Load chat history between the current user and the friend
    messages = ChatMessages.query.filter(
        ((ChatMessages.sender == user_id) & (ChatMessages.receiver == friend_id)) |
        ((ChatMessages.sender == friend_id) & (ChatMessages.receiver == user_id))
    ).order_by(ChatMessages.timestamp.asc()).all()
    

    messages_data = [{'sender': msg.sender, 'message': msg.message} for msg in messages]
    
    friend = ChatFriends.query.filter((ChatFriends.username == user_id) & (ChatFriends.friend_username == friend_id))
    a = friend[0]
    if(a.notifications > 0):
        a.notifications = 0
        db.session.add(a)
        db.session.commit()
    
    return jsonify(messages=messages_data)

@chatWithFriends_pg.route('/clearChatMessages/<friend_id>',methods=['GET','POST'])
def clearChat(friend_id):
    user_id = session.get('username')
    # Load chat history between the current user and the friend
    messages = ChatMessages.query.filter(
        ((ChatMessages.sender == user_id) & (ChatMessages.receiver == friend_id)) |
        ((ChatMessages.sender == friend_id) & (ChatMessages.receiver == user_id))
    ).all()
    
    for user in messages:
        db.session.delete(user)
    db.session.commit()
    return "Cleared"

@socketio.on('send_message')
def handle_send_message(data):
    sender = session.get('username')
    receiver = data['friend_id']
    message = data['message']

    # Store the message in the database
    if(receiver == sender):
        new_message = ChatMessages(sender=sender, receiver=receiver, message=message)
        db.session.add(new_message)
        db.session.commit()
    elif(receiver in connectedUsers):
        new_message = ChatMessages(sender=sender, receiver=receiver, message=message)
        db.session.add(new_message)
        db.session.commit()
        # Emit the message to the receiver if they are online
        receiver_sid = connectedUsers[receiver]
        emit('receive_message', {'sender': sender, 'message': message}, room=receiver_sid)
    else:
        new_message = ChatMessages(sender=sender, receiver=receiver, message=message)
        friend = ChatFriends.query.filter((ChatFriends.username == receiver) & (ChatFriends.friend_username == sender))[0]
        friend.notifications = friend.notifications+1
        db.session.add(friend)
        db.session.add(new_message)
        db.session.commit()

@socketio.on('join')
def on_join(data):
    connectedUsers[data] = request.sid
    
# Handle user disconnection
@socketio.on('disconnect')
def handle_disconnect():
    # user_sid = request.sid
    username = session.get('username')
    # for key,value in connected_users.items():
    #     if value == user_sid:
    #         username = key
    
    # print(connected_users)
    if username in connectedUsers:
        connectedUsers.pop(username)
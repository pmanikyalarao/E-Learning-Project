from flask import Flask
from .extensions import *

def createApp():
    app = Flask(__name__)
    
    #data base configuration
    app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///elearning.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    #main configuration
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 465
    app.config['MAIL_USERNAME'] = 'YOUR MAIL ID TO SEND OTPS'
    app.config['MAIL_PASSWORD'] = 'YOUR MAIL PASSWORD'
    app.config['MAIL_USE_TLS'] = False
    app.config['MAIL_USE_SSL'] = True
    app.config['MAIL_DEFAULT_SENDER'] = 'YOUR MAIL ID TO SEND OTPS'
    
    #secret_key
    app.secret_key = 'elearning website'
    
    #initializing app
    db.init_app(app)
    mail.init_app(app)
    socketio.init_app(app)
    app.app_context().push()
    
    #importing blueprints
    from .beforeLogin.routes import beforeLoginHome_pg
    from .afterLogin.routes import afterLoginHome_pg
    from .virtualClassRoom.routes import virtualClassRoom_pg
    from .chatbot.routes import chatbot_pg
    from .chatWithFriends.routes import chatWithFriends_pg
    from .courses.routes import courses_pg
    
    #registering blueprints
    app.register_blueprint(beforeLoginHome_pg)
    app.register_blueprint(afterLoginHome_pg)
    app.register_blueprint(virtualClassRoom_pg)
    app.register_blueprint(chatbot_pg)
    app.register_blueprint(chatWithFriends_pg)
    app.register_blueprint(courses_pg)
    

    return app

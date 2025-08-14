from flask import Blueprint,render_template,url_for,redirect,request,jsonify,session
from random import choice
import google.generativeai as genai
from models.messagesOfChatbot import ChatbotMessages
from ..extensions import db
import re
from apikeys import googleAPIKey

# configure the api key for gemini ai
genai.configure(api_key=googleAPIKey)
#model of the gemini ai
model = genai.GenerativeModel(model_name='gemini-1.5-flash')

chatbot_pg = Blueprint("chatbot_pg",
                       __name__,
                       template_folder="templates",
                       static_folder="chatbotStatic")

# botMsg = ["The Full form of HTML is hyper text markap language..",
#           "What is purpose of HTML","The pourpose of HTML language is used to create a webpage in WWW(world wide web)",
#           "Css is a programing language which is used to apply the style to html page.CSS stands for cascading style sheet."]

# chat = []

#mainChatBotPage
@chatbot_pg.route("/ChatbotPage")
def chatbotWebPage():
    return render_template("mainChatbot.html",chat = ChatbotMessages.query.filter(ChatbotMessages.user_id == session.get('username')).order_by(ChatbotMessages.timestamp.asc()).all())


#commonChatBotPage
@chatbot_pg.route("/commonChatbotPage",methods=['GET','POST'])
def commonChatbotWebPage():
    return render_template("commonChatbot.html",chat = ChatbotMessages.query.filter(ChatbotMessages.user_id == session.get('username')).order_by(ChatbotMessages.timestamp.asc()).all())

#hadling chat messages 
@chatbot_pg.route("/chatbotMessage",methods=["GET","POST"])
def chatbotMessage():
    msg = request.form.get("message")
    response = model.generate_content(msg)
    # bot = choice(botMsg)
    bot = response.text
    
    # Regex patterns
    bold_pattern = r'\*\*(.*?)\*\*'        # Match **text**
    italic_pattern = r'\*(.*?)\*'           # Match *text*
    bullet_point_pattern = r'^\s*\*\s'      # Match bullet points starting with *

    # Replacing **text** with <b>text</b>
    formatted_text = re.sub(bold_pattern, r'<b>\1</b>', bot)

    # Replacing *text* with <i>text</i>
    formatted_text = re.sub(italic_pattern, r'<i>\1</i>', formatted_text)

    # Replacing bullet points (*) with <li>text</li> (HTML list item)
    formatted_text = re.sub(bullet_point_pattern, r'<li>', formatted_text, flags=re.MULTILINE)

    # Convert list items into <ul> format for structured bullets
    formatted_text = re.sub(r'((<li>.*?</li>\n)+)', r'<ul>\n\1</ul>\n', formatted_text)

    
    newChat = ChatbotMessages(user_message=msg,bot_message=formatted_text,user_id=session.get('username'))
    db.session.add(newChat)
    db.session.commit()
    # data = {"user_id":session.get('username'),"user":msg,"bot":bot}
    # chat.append(data)
    return formatted_text


#commonChatBotPage
@chatbot_pg.route("/clearChatbotMessages",methods=['GET','POST'])
def clearChatbotMessages():
    messages = ChatbotMessages.query.filter(ChatbotMessages.user_id == session.get('username'))
    for user in messages:
        db.session.delete(user)
    db.session.commit()
    return "Cleared"
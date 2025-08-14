from flask import flash,Blueprint,render_template,redirect,url_for,session,request
from flask_mail import Message

beforeLoginHome_pg = Blueprint(
                        "beforeLoginHome_pg",
                        __name__,
                        template_folder="templates",
                        static_folder="beforeStatics"
                    )

#to check the session 
def checkSession():
    if session.get("email"):
        return True
    return False

#generate otp
def generateOtp():
    from random import randint
    return randint(1000,9000)

#sending otp to mail
def sendOTPMail(receiverMail):
    from myBlueprints import mail
    otp = generateOtp()
    msg = Message('Your E-Learning Platform Verification Code',recipients=[receiverMail])
    msg.html = render_template('mailBody.html',otp=otp)
    try:
        mail.send(msg)
    except Exception:
        return False
    session['otp'] = otp
    return True

#home page
@beforeLoginHome_pg.route("/")
@beforeLoginHome_pg.route('/home')
def home():
    if checkSession():
        return redirect(url_for('afterLoginHome_pg.home'))
    return render_template('home.html')

#courses page
@beforeLoginHome_pg.route('/courses')
def courses():
    if checkSession():
        return redirect(url_for('afterLoginHome_pg.home'))
    return render_template("courses.html")

#contactus page
@beforeLoginHome_pg.route('/contactus')
def contactus():
    if checkSession():
        return redirect(url_for('afterLoginHome_pg.home'))
    return render_template('contactus.html')

#aboutus page
@beforeLoginHome_pg.route('/aboutus')
def aboutus():
    if checkSession():
        return redirect(url_for('afterLoginHome_pg.home'))
    return render_template('aboutus.html')

#login page
@beforeLoginHome_pg.route('/login')
def login():
    if checkSession():
        return redirect(url_for('afterLoginHome_pg.home'))
    return render_template('login.html')

#for login to the website
@beforeLoginHome_pg.route("/loginSubmited",methods=['POST'])
def loginSubmited():
    email = request.form.get('email')
    password = request.form.get('password')
    from models.userDetailsForLogin import UserDetails
    user = UserDetails.query.filter_by(email = email).first()
    if user:
        if password==user.password:
            session['email'] = email
            session['username'] = user.username
            return redirect("/loginHome")
        else:
            flash("Incorrect Password!")
    else:
        flash("Incorrect email and password!")
    return redirect("/login")

#signup page
@beforeLoginHome_pg.route('/signup')
def signup():
    if checkSession():
        return redirect(url_for('afterLoginHome_pg.home'))
    # flash("Incorrect email!")
    return render_template('signup.html')

#geting the user data form sign up page
@beforeLoginHome_pg.route('/signupData',methods=['POST'])
def signUpData():
    name = request.form.get('name')
    email = request.form.get('email')
    password = request.form.get('password')
    phone = request.form.get('phone')
    from models.userDetailsForLogin import UserDetails
    from ..extensions import db
    exist = UserDetails.query.filter_by(email=email).first()
    if exist:
        flash("email is already existing!")
        return redirect("/signup")
    else:
        session['createEmail'] = email
        session['createName'] = name
        session['createPassword'] = password
        session['createPhone'] = phone
    return redirect(url_for('beforeLoginHome_pg.username'))

#username page
@beforeLoginHome_pg.route('/username')
def username():
    return render_template('username.html')

#to create the user name 
@beforeLoginHome_pg.route("/createUsername",methods=['POST'])
def createUsername():
    username = request.form.get('username')
    from models.userDetailsForLogin import UserDetails
    from ..extensions import db
    exist = UserDetails.query.filter_by(username=username).first()
    if exist:
        flash("Username is already existing!")
        return redirect("/username")
    else:
        session['createUsername'] = username
        session['otpType'] = url_for('beforeLoginHome_pg.signUpOtpValidatePage')
        check = sendOTPMail(session.get('createEmail'))
        if check:
            session['otpType'] = url_for('beforeLoginHome_pg.signUpOtpValidatePage')
        else:
            flash("Invalid email!")
            return redirect(url_for('beforeLoginHome_pg.signup'))
    return redirect(url_for('beforeLoginHome_pg.otpPage'))

#validate otp for signUp page
@beforeLoginHome_pg.route("/signUpOptValidatePage",methods=['POST'])
def signUpOtpValidatePage():
    if request.form.get('otp') == str(session.get('otp')):
        session.pop('otpType',None)
        session.pop('otp',None)
        return redirect(url_for('beforeLoginHome_pg.createUser'))
    else:
        flash("Incorrect OTP!")
    return redirect(url_for('beforeLoginHome_pg.otpPage'))

#to create the user account
@beforeLoginHome_pg.route("/createUser")
def createUser():
    from models.userDetailsForLogin import UserDetails
    from ..extensions import db
    user = UserDetails(name=session['createName'],email=session['createEmail'],password=session['createPassword'],phone=session['createPhone'],username=session['createUsername'])
    db.session.add(user)
    db.session.commit()
    session.pop('createName',None)
    session.pop('createEmail',None)
    session.pop('createPassword',None)
    session.pop('createPhone',None)
    session.pop('createUserame',None)
    flash("Registered successfully!")
    return redirect("/login")


#otp page
@beforeLoginHome_pg.route("/optPage")
def otpPage():
    return render_template("otp.html")

#resend otp to mail
@beforeLoginHome_pg.route('/resendOtp')
def resendOtp():
    if session.get('otpType') == url_for('beforeLoginHome_pg.signUpOtpValidatePage'):
        check = sendOTPMail(session.get('createEmail'))
        if check:
            flash('OTP is resend to your mail!')
        else:
            flash("OTP doesn't send!")
            return redirect(url_for('beforeLoginHome_pg.signup'))
    elif session.get('otpType') == url_for('beforeLoginHome_pg.forgotOtpValidatePage'):
        check = sendOTPMail(session.get('forgotEmail'))
        if check:
            flash('OTP is resend to your mail!')
        else:
            flash("OTP doesn't send!")
            return redirect(url_for('beforeLoginHome_pg.forgot'))
    else:
        return redirect(url_for('beforeLoginHome_pg.home'))
    return redirect(url_for('beforeLoginHome_pg.otpPage'))

#forgot page
@beforeLoginHome_pg.route("/forgotPassword")
def forgot():
    return render_template("forgotPassword.html")

#geting email from forgot page
@beforeLoginHome_pg.route("/handleForgotPassword",methods=['POST'])
def handleForgotPassword():
    email = request.form.get('email')
    from models.userDetailsForLogin import UserDetails
    from ..extensions import db
    exist = UserDetails.query.filter_by(email=email).first()
    if exist:
        session['forgotEmail'] = email
        check = sendOTPMail(email)
        if check:
            session['otpType'] = url_for('beforeLoginHome_pg.forgotOtpValidatePage')
        else:
            flash("OTP doesn't send!")
            return redirect(url_for('beforeLoginHome_pg.forgot'))
        return redirect(url_for('beforeLoginHome_pg.otpPage'))
    else:
        flash("Invalid email!")
        return redirect('/forgotPassword')
    
#validate otp for forgot password page
@beforeLoginHome_pg.route("/forgotOptValidatePage",methods=['POST'])
def forgotOtpValidatePage():
    # print(type(request.form.get('otp')))
    # print(type(session.get('otp')))
    if request.form.get('otp') == str(session.get('otp')):
        session.pop('otp',None)
        return redirect(url_for('beforeLoginHome_pg.resetPassword'))
    else:
        flash("Incorrect OTP!")
        return redirect(url_for('beforeLoginHome_pg.otpPage'))
    return render_template("otp.html")
    
#reset password page
@beforeLoginHome_pg.route("/resetPassword")
def resetPassword():
    return render_template('resetPassword.html')

#createing new password
@beforeLoginHome_pg.route("/createNewPassword",methods=['POST'])
def createNewPassword():
    email = session.get('forgotEmail')
    newPassword = request.form.get('newPassword')
    confirmPassword = request.form.get('confirmPassword')
    from models.userDetailsForLogin import UserDetails
    from ..extensions import db
    exist = UserDetails.query.filter_by(email=email).first()
    if newPassword == confirmPassword:
        exist.password = newPassword
        db.session.add(exist)
        db.session.commit()
        session.pop('forgotEmail',None)
        session.pop('otpType',None)
        flash("password is changed!")
        return redirect(url_for('beforeLoginHome_pg.login'))
    else:
        flash("new password and confirm password doesn't match")
    return redirect('/resetPassword')
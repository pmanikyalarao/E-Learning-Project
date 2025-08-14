from flask import Blueprint,render_template,redirect,request,url_for,session

afterLoginHome_pg = Blueprint(
                    "afterLoginHome_pg",
                    __name__,
                    template_folder='templates',
                    static_folder="afterStatics"
                )
def checkAfterLoginSession():
    if not session.get('email'):
        return True
    return False

@afterLoginHome_pg.route("/loginHome")
def home():
    if checkAfterLoginSession():
        return redirect(url_for('beforeLoginHome_pg.login'))
    return render_template("homeAfterLogin.html")

@afterLoginHome_pg.route("/loginProfile")
def profile():
    if checkAfterLoginSession():
        return redirect(url_for('beforeLoginHome_pg.login'))
    from models.userDetailsForLogin import UserDetails
    return render_template("profile.html",details = UserDetails.query.filter_by(email = session['email']).first())

@afterLoginHome_pg.route('/logout')
def logout():
    session.pop('email',None)
    session.pop('username',None)
    return redirect(url_for('beforeLoginHome_pg.login'))

@afterLoginHome_pg.route('/afterLoginAbout')
def afterLoginAbout():
    return render_template('loginAbout.html')
from flask import Blueprint,redirect,url_for,render_template,session,flash
from Expensetracker.forms import login_forms,forget_forms,otp_forms,newpassword_forms
from Expensetracker.models import signin_db
from Expensetracker import db
import random

login_bp = Blueprint("login",__name__)


# login
@login_bp.route("/",methods=["POST","GET"])
def login_():
    form = login_forms()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        user = signin_db.query.filter_by(email = email).first()
        if user and user.password == password:
        
            session["user_id"] = user.id
            return redirect(url_for("profile.profile_"))
        else:
            flash("Your email or password is Incorrect")
            return redirect(url_for("login.login_" ))
    return render_template("login.html",form = form)

# check email


@login_bp.route("/forget-password", methods=["POST","GET"])
def check_email(): 
    
    email_form = forget_forms()
    otp_form = otp_forms()

    if email_form.validate_on_submit():
        email = email_form.email.data

        user = signin_db.query.filter_by(email = email).first()
        if user:
            session["user_email"] = user.email
            session["user_id"] = user.id
            session["otp"] = random.randint(1000,9999)
            print(session["otp"])
            return redirect(url_for("login.forget"))
        
        flash("Email incorrect")
        return redirect(url_for("login.check_email"))
    return render_template("forget_password.html",emailform = email_form,otpform = otp_form,available = False)

# forget password
@login_bp.route("/forget", methods=["POST","GET"])
def forget():
    if "user_email" not in session:
        return redirect(url_for("login.check_email"))

    email_form = forget_forms()
    otp_form = otp_forms()

# readonly email ke liye form me value daal do
    email_form.email.data = session["user_email"]
    
    if otp_form.validate_on_submit():
        otp = otp_form.otp.data

        if otp == session["otp"]:
            session["otp_verified"] = True
            return redirect(url_for("login.new_password"))
        
        flash("OTP is incorrect ")
        return redirect(url_for("login.forget"))
    
    return render_template("forget_password.html",otpform = otp_form,emailform = email_form,available = True)

# back to login
@login_bp.route("/back-to-login",methods=["POST","GET"])
def back_login():
    session.pop("user_email", None)
    session.pop("otp",None)
    session.pop("otp_verified",None)
    return redirect(url_for("login.login_"))

# New password
@login_bp.route("/new-password",methods=["POST","GET"])
def new_password():

    if not session.get("otp_verified"): # true/false ke liye aise use
        return redirect(url_for("login.login_"))
    
    if "user_id" not in session:
        return redirect(url_for("login.login_"))
    
    user = signin_db.query.get(session["user_id"])
    form = newpassword_forms()
    if form.validate_on_submit():
        newpassword = form.new_password.data
        confirm_password = form.confirm_password.data
        if newpassword != confirm_password:
            flash("password do not match, Try Again")
            return redirect(url_for("login.new_password"))
        else:
            user.password = newpassword
            session.pop("user_email", None)
            session.pop("user_id",None)
            session.pop("otp",None)
            session.pop("otp_verified",None)
            db.session.commit()
            return redirect(url_for("login.login_"))
    return render_template("newpassword.html",form = form)
        
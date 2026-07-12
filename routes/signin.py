from flask import Blueprint,redirect,url_for,render_template,flash
from Expensetracker.forms import signin_forms
from Expensetracker.models import signin_db
from Expensetracker import db

signin_bp = Blueprint("signin",__name__)

@signin_bp.route("/signin",methods=["POST","GET"])
def signin_():
    form = signin_forms()
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        password = form.password.data
        confirm_password = form.confirm_password.data
        user = signin_db.query.filter_by(email = email).first()
        if user:
            flash("Email is already registered")
            return redirect(url_for("signin.signin_"))

        if password != confirm_password:
            flash("Password is Incorrect")
            return redirect(url_for("signin.signin_"))

        new_user = signin_db(
            name = name,
            email = email,
            password = password
        )
        db.session.add(new_user)
        db.session.commit()
        flash("You Registered Successfully")
        return redirect(url_for("login.login_"))
    return render_template("signin.html",form = form)
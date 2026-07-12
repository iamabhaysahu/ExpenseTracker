from flask import Blueprint,redirect,url_for,render_template,session,request,flash
from Expensetracker.forms import profile_forms,modified_forms,editbalance
from Expensetracker.models import signin_db,profile_db
from Expensetracker import db
from sqlalchemy import func
profile_bp = Blueprint("profile",__name__)
 
@profile_bp.before_request
def check_login():
    if "user_id" not in session:
        return redirect(url_for("login.login_"))

@profile_bp.route("/profile", methods=["POST","GET"])
def profile_():
    form = profile_forms()
    user = signin_db.query.get(session["user_id"])
    user_item = profile_db.query.filter_by(user_id = session["user_id"]).order_by(profile_db.id.desc()).limit(3)
    result = db.session.query(func.sum(profile_db.amount),func.count(profile_db.id),func.avg(profile_db.amount)).filter_by(user_id = session["user_id"]).first()
    total = result[0]
    if total == None:
        total = 0.0
    else:
        total = result[0]
    count = result[1]
    leftamount = user.income - total
    average_money = result[2]
 

    # leftamount =  user.income- total
    result = db.session.query(signin_db).all()
    if form.validate_on_submit():
        amount = form.amount.data
        categories = form.categories.data
        note = form.note.data
        user_data = profile_db(
            amount = amount,
            categories = categories,
            note = note,
            user_id = session['user_id']
        )
        flash("Expense is Registered")
        db.session.add(user_data)
        db.session.commit()
        return redirect(url_for("profile.profile_"))
    return render_template("profile.html",form = form,user = user,leftamount= leftamount,items=user_item,total = total,count = count)

@profile_bp.route("/delete/<int:task_id>",methods=["POST","GET"])
def delete_task(task_id):
    task = profile_db.query.get(task_id)
    if task:
        db.session.delete(task)
        db.session.commit()
    return redirect(url_for("profile.show_database"))

@profile_bp.route("/modified/<int:task_id>",methods=["POST","GET"])
def modified_task(task_id):
    form = modified_forms()
    task = profile_db.query.get(task_id)

    if request.method == "GET":
        form.amount.data = task.amount
        form.categories.data = task.categories
        form.note.data  = task.note
        form.datetime.data = task.datetime
    if form.validate_on_submit():
        task.amount =  form.amount.data
        task.categories = form.categories.data
        task.note = form.note.data
        task.datetime = form.datetime.data
        db.session.commit()
        flash("Data Modified successfully")
        return redirect(url_for("profile.profile_"))
    return render_template("record_modified.html",form = form)

@profile_bp.route("/logout",methods=["POST"])
def logout():
    session.pop("user_id",None)
    flash("logout successfully")
    return redirect(url_for("login.login_"))

@profile_bp.route("/see-database",methods=["GET","POST"])
def show_database():
    page = request.args.get("page",1,type=int)
    user_items = profile_db.query.filter_by(user_id = session["user_id"]).order_by(profile_db.id.desc()).paginate(page = page,per_page = 9)
    form = profile_forms()
    return render_template("show_database.html",user_item = user_items,form = form)

@profile_bp.route("/edit-balance",methods=["POST","GET"])
def edit_bal():
    form = editbalance()
    if form.validate_on_submit():
        user_id  = session["user_id"]
        user = signin_db.query.get(user_id)
        user.income = form.income.data
        db.session.add(user)
        db.session.commit()
        flash("Add successfully Income")
        return redirect(url_for("profile.profile_"))
    return render_template("add_income.html",form = form)

@profile_bp.route("/filter",methods=["GET",])
def filter_data():

    note = request.args.get("search")
    categories = request.args.get("categories")
    date = request.args.get("datetime")

    query = profile_db.query.filter(profile_db.user_id == session["user_id"])

    if note:
        query = query.filter(profile_db.note.ilike(f"%{note}%"))
    
    if categories:
        query = query.filter(profile_db.categories == categories)
    
    if date:
        query = query.filter(func.date(profile_db.datetime) == date)
    
    
    user_item = query.order_by(profile_db.id.desc()).all()


    return render_template("show_database.html",user_item = user_item)

    # if not note and not categories and not date:
    #     return redirect(url_for("profile.show_database"))
    # elif date and not categories and not note:
    #     user_item = profile_db.query.filter(profile_db.user_id ==session["user_id"],func.date(profile_db.datetime) == date).all()
    # elif note and not categories:
    #     user_item = profile_db.query.filter(profile_db.user_id == session["user_id"],profile_db.note.ilike(f"%{note}%")).all()

    # elif not note and categories:
    #     user_item = profile_db.query.filter(profile_db.user_id == session["user_id"],profile_db.categories == categories).all()
        
    # else:
    #     user_item = profile_db.query.filter(profile_db.user_id == session["user_id"],profile_db.note.ilike(f"%{note}%"),profile_db.categories == categories).all()
    # return render_template("show_database.html",user_item = user_item)

    

# IMPORTANT NOTE
# jab hum aggrate functions use karte hai to agar hum 1 chiz hi use kar rahe hai to .scalar() use karte hai 
# Kyunki id Primary Key hai aur get() hamesha Primary Key se ek hi record nikalta hai.

# db = SQLAlchemy(app)
# Yahan app ko argument ke roop me pass kiya hai.

# Q: API me database object ko direct return kyu nahi kar sakte?
# A: Kyuki browser SQLAlchemy object nahi samajhta. Browser ko JSON format me data chahiye.

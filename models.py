from Expensetracker import db
from datetime import datetime
class signin_db(db.Model):
    id = db.Column(db.Integer,primary_key= True)
    name = db.Column(db.String(50),nullable=False)
    email = db.Column(db.String(100),nullable= False, unique = True)
    password = db.Column(db.String(100),nullable= False) 
    income = db.Column(db.Float,default=0.0)
    
class profile_db(db.Model):
    id = db.Column(db.Integer,primary_key= True)
    user_id = db.Column(db.Integer,db.ForeignKey("signin_db.id"))
    amount = db.Column(db.Float,nullable = False)
    categories = db.Column(db.String(100))
    note = db.Column(db.String(250),default="None")
    
    datetime = db.Column(db.DateTime,default = datetime.now)
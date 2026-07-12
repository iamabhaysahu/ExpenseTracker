from flask_wtf import FlaskForm
from wtforms import PasswordField,SubmitField,StringField,EmailField,FloatField,SelectField,DateTimeField,IntegerField
from wtforms.validators import InputRequired,Length

class signin_forms(FlaskForm):
    name = StringField("NAME",validators=[InputRequired()])
    email = EmailField("E-MAIL",validators=[InputRequired()])
    password = PasswordField("PASSWORD",validators=[InputRequired(),Length(min=6)])
    confirm_password = PasswordField("PASSWORD",validators=[InputRequired(),Length(min=6)])
    submit = SubmitField("SIGNIN")

class login_forms(FlaskForm):
    email = EmailField("E-MAIL",validators=[InputRequired()])
    password = PasswordField("PASSWORD",validators=[InputRequired()])
    submit = SubmitField("LOGIN")

class profile_forms(FlaskForm):
    amount = FloatField("amount",validators=[InputRequired()])
    categories = SelectField("categories",choices=[("Other","Other"),('Travel',"Travel"),("Shopping","Shopping"),("Food","Food")])
    note = StringField("Note")
    submit = SubmitField("SAVE Expense")

class modified_forms(FlaskForm):
    amount = FloatField("amount",validators=[InputRequired()])
    categories = SelectField("categories",choices=[("Other","Other"),('Travel',"Travel"),("Shopping","Shopping"),("Food","Food")])
    note = StringField("Note")
    submit = SubmitField("Modified details")
    datetime = DateTimeField("Datetime")

class forget_forms(FlaskForm):
    email = EmailField("E-MAIL",validators=[InputRequired()])
    submit = SubmitField("check email")
    

class otp_forms(FlaskForm):
    otp = IntegerField("otp",validators=[InputRequired()])
    submit = SubmitField("check otp")

class newpassword_forms(FlaskForm):
    new_password = PasswordField("PASSWORD",validators=[InputRequired(),Length(min=6)])
    confirm_password = PasswordField("PASSWORD",validators=[InputRequired(),Length(min=6)])
    submit = SubmitField("save password")

class editbalance(FlaskForm):
    income = FloatField("amount",validators=[InputRequired()])
    submit = SubmitField("Save Income")

from market.model import User
from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,HiddenField
from wtforms.validators import Length,EqualTo,Email,DataRequired,ValidationError

class RegisterForm(FlaskForm):
    def validate_username(self,name):
        user = User.query.filter_by(username=name.data).first()
        if user:
            raise ValidationError("Username already Exist!,please create a different username:")
            
    def validate_email(self,email):
        email = User.query.filter_by(email=email.data).first()
        if email:
            raise ValidationError("Email already Exist!,please create a different email")


    
    username = StringField(label="User Name:",validators=[Length(min=2,max=30),DataRequired()])
    email = StringField(label="Email Address:",validators=[Email(),DataRequired()])
    password1 = PasswordField(label="Password:",validators=[Length(min=6,max=40),DataRequired()])
    password2 = PasswordField(label="Confirm Password:",validators=[EqualTo('password1'),DataRequired()])
    submit = SubmitField(label="Create Account:")

class LoginForm(FlaskForm):
    username = StringField(label="User Name:",validators=[DataRequired()])
    password = PasswordField(label="Confirm Password:",validators=[DataRequired()])
    submit = SubmitField(label="Sign in")

class PurchaseItemForm(FlaskForm):
    submit = SubmitField(label="Purchase Item")
 
class SellItemForm(FlaskForm):
    submit = SubmitField(label="Sell Item")
 




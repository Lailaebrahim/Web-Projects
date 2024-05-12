from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flaskblog import db
from flaskblog.models import User


#Importing the FlaskForm class which defines the base for creating forms in Flask
#Then Defining Classes that inheratis from it add add the fields required and the desired constaints on the inpt values 
#Using the validators to check that the input value follow the constraints and generate errors to be displayed to instruct user to fix them so form submits
class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[
                           Length(min=2, max=20), DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    confirm_password = PasswordField("Confirm Password", validators=[
                                     DataRequired(), EqualTo('password')])
    submit = SubmitField("Sign Up")
    
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError("This username is taken. Please choose another one!")
    
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError("This email already have an account. Please choose another one or Login to your account")    


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember = BooleanField('Remember Me?')
    submit = SubmitField("Login")

    #def validate_email(self, email):
    #    user = User.query.filter_by(email=email.data).first()
        #if user is None:
         #   raise ValidationError("Invalid Email")
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo

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


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember = BooleanField('Remember Me?')
    submit = SubmitField("Login")

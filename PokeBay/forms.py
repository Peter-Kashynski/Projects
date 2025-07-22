from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, RadioField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo, length, ValidationError 
from datetime import datetime 
from email_validator import validate_email, EmailNotValidError 
from flask_login import LoginManager, UserMixin 
from werkzeug.security import generate_password_hash, check_password_hash    

class RegistrationForm(FlaskForm):
  username = StringField('Username', validators=[DataRequired(), length(min=3, max=11)])
  email = StringField('Email', validators=[DataRequired(), Email()])
  shipping_address = StringField('Shipping Address', validators=[length(max=128)])
  password = PasswordField('Password', validators=[DataRequired(), length(min=4, max=20)])
  password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password', message='passwords must match')])
  submit = SubmitField('Register')  

  def __repr__(self):
    return '<User {}>'.format(self.username)

  def set_password(self, password):
    self.password_hash = generate_password_hash(password)

  def check_password(self, password):
    return check_password_hash(self.password_hash, password) 
  
class LoginForm(FlaskForm):
  email = StringField('Email', validators=[DataRequired(), Email()])
  password = PasswordField('Password', validators=[DataRequired()])
  remember = BooleanField('Remember Me')
  submit = SubmitField('Login')  

class DeleteForm(FlaskForm):
    submit = SubmitField("Delete all users?") 

class LogoutForm(FlaskForm): 
    submit = SubmitField('Logout') 

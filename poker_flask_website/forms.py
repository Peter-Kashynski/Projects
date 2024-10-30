
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, RadioField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo, length, ValidationError 
from datetime import datetime 
from flask import Flask, render_template, redirect, url_for, flash     
from email_validator import validate_email, EmailNotValidError 
from helper import card_1, card_2  
from flask_login import LoginManager, UserMixin 
from werkzeug.security import generate_password_hash, check_password_hash   







suits = [("Diamond", "Diamond"), ("Heart", "Heart"), ("Club", "Club"), ("Spade", "Spade")]  
numbers = [(2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10), ("J", "J"), ("Q", "Q"), ("K", "K"), ("A", "A")] 


class CommentForm(FlaskForm):
  comment = StringField("Comment", validators=[DataRequired()])
  submit = SubmitField("Add Comment")  


class RegistrationForm(FlaskForm):
  username = StringField('Username', validators=[DataRequired(), length(min=3, max=15)])
  email = StringField('Email', validators=[DataRequired(), Email()])
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

class CardForm(FlaskForm):
    card_1_rank = RadioField('Card 1 Rank', choices=numbers, validators=[DataRequired()])
    card_1_suit = RadioField('Card 1 Suit', choices=suits, validators=[DataRequired()])
    card_2_rank = RadioField('Card 2 Rank', choices=numbers, validators=[DataRequired()])
    card_2_suit = RadioField('Card 2 Suit', choices=suits, validators=[DataRequired()])
    submit = SubmitField('Submit')


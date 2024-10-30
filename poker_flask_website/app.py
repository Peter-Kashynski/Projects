

from flask import Flask, request, render_template, redirect, url_for, flash    
from helper import card_1, card_2, equity_dictionary_offsuit, equity_dictionary_suited, get_equity  
from datetime import datetime 
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, current_user, login_user, logout_user, login_required 
from werkzeug.security import generate_password_hash, check_password_hash
from email_validator import validate_email, EmailNotValidError    
from forms import CardForm, RegistrationForm, LoginForm  
import random 
from os import environ  
import os


app = Flask(__name__)
app.config['SECRET_KEY'] = 'nuh-uh'
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DATABASE_URL') or 'sqlite:///myDB.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  

db = SQLAlchemy(app)
 # This line creates the database tables
  
login_manager = LoginManager()
login_manager.init_app(app)

# Initialize the extensions with the app
login_manager.login_view = 'login' # type: ignore
login_manager.login_message = "Please log in to access this page."

class User(UserMixin, db.Model):
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(64), index=True, unique=True) 
  email = db.Column(db.String(120), index=True, unique=True) 
  password_hash = db.Column(db.String(128), index=True, unique=True)  
  joined_at = db.Column(db.DateTime(), index=True, default=datetime.utcnow)  

  def __repr__(self):
    return '<User {}>'.format(self.username)

  def set_password(self, password):
    self.password_hash = generate_password_hash(password)

  def check_password(self, password):
    return check_password_hash(self.password_hash, password) 

with app.app_context():
  db.create_all()  

#user loader 
@login_manager.user_loader
def load_user(user_id):  
  return User.query.get(int(user_id))  

# custom message for unloggedin users   
@login_manager.unauthorized_handler 
def unauthorized(): 
   return render_template('loginfail.html')


@app.route('/') 
def root_redirect():
    return redirect(url_for('login'))  

@app.route('/welcome') 

@app.route('/register', methods=['GET', 'POST'])
def register(): 
  form = RegistrationForm(csrf_enabled=False)
  if form.validate_on_submit(): 
    existing_user = User.query.filter_by(email=form.email.data).first()
    if existing_user:
        form.email.errors.append("Email already in use. Please choose a different one.")
        return render_template('register.html', form=form)
    user = User(username=form.username.data, email=form.email.data) # type: ignore
    user.set_password(form.password.data)
    db.session.add(user)
    db.session.commit()
  return render_template('register.html', title='Register', form=form)  


# login route
@app.route('/login', methods=['GET','POST'])
def login():   
  form = LoginForm(csrf_enabled=False) 
  user = None
  if form.validate_on_submit():
    user = User.query.filter_by(email=form.email.data).first() 
    if user and user.check_password(form.password.data):
        login_user(user, remember=form.remember.data)  
        return redirect(url_for('index'))
  return render_template('login.html', form=form, current_user=user) 


#add logout button 
@app.route('/logout', methods=['GET','POST'])
def logout():
    logout_user()
    #flash('You have been logged out.', 'success')
    return redirect(url_for('login'))
  

@app.route('/home')   
@login_required 
def index():  
    return render_template('index.html') 

@app.route('/preflopcharts')  
@login_required 
def preflop(): 
    return render_template('charts.html') 

@app.route('/tablepositions')   
@login_required
def positions(): 
    return render_template('positions.html') 


@app.route('/equitycalculator', methods=["GET", "POST"])   
@login_required 
def calculator():   
    equity = 0
    card_form = CardForm(csfr_enabled=True)   

    card_1_rank = None
    card_1_suit = None
    card_2_rank = None
    card_2_suit = None 
    
    if card_form.validate_on_submit():    

      card_1_rank = card_form.card_1_rank.data 
      card_1_suit = card_form.card_1_suit.data 

      card_2_rank = card_form.card_2_rank.data 
      card_2_suit = card_form.card_2_suit.data  

      equity = get_equity(card_1_rank, card_1_suit, card_2_rank, card_2_suit)


    return render_template("equity.html",  
                           card_form=card_form, 
                           card_1_suit=card_1_suit,  
                           card_1_rank=card_1_rank,  
                           card_2_suit=card_2_suit, 
                           card_2_rank=card_2_rank,
                           equity=equity
                           )  



@app.route('/equitycalculator/whatisequity?')  
@login_required 
def equity(): 
    return render_template("what_is_equity.html")

@app.route('/grid') 
def grid(): 
    return render_template("grid.html")  

@app.route('/users')  
@login_required 
def users():   
   current_users = User.query.all()
   return render_template("users.html", current_users=current_users)


if __name__ == "__main__":
    app.run(debug=True)




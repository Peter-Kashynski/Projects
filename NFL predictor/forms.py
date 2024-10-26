 

from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, SubmitField, TextAreaField, RadioField, PasswordField, BooleanField, SelectField 
from wtforms.validators import DataRequired, NumberRange 


home_teams = [('crd', 'Arizona Cardinals'), ('atl', 'Atlanta Falcons'),  
              ('rav', 'Baltimore Ravens'), ('buf', 'Buffalo Bills'), 
              ('car', 'Carolina Panthers'), ('chi', 'Chicago Bears'), 
              ('cin', 'Cincinnati Bengals'), ('cle', 'Cleveland Browns'), 
              ('dal', 'Dallas Cowboys'), ('den', 'Denver Broncos'), 
              ('det', 'Detroit Lions'), ('gnb', 'Green Bay Packers'), 
              ('htx', 'Houston Texans'), ('clt', 'Indianapolis Colts'), 
              ('jax', 'Jacksonville Jaguars'), ('kan', 'Kansas City Chiefs'), 
              ('rai', 'Las Vegas Raiders'), ('sdg', 'Los Angeles Chargers'), 
              ('ram', 'Los Angeles Rams'), ('mia', 'Miami Dolphins'), 
              ('min', 'Minnesota Vikings'), ('nwe', 'New England Patriots'), 
              ('nor', 'New Orleans Saints'), ('nyg', 'New York Giants'), 
              ('nyj', 'New York Jets'), ('phi', 'Philadelphia Eagles'), 
              ('pit', 'Pittsburgh Steelers'), ('sfo', 'San Francisco 49ers'), 
              ('sea', 'Seattle Seahawks'), ('tam', 'Tampa Bay Buccaneers'), 
              ('oti', 'Tennessee Titans'), ('was', 'Washington Commanders')]  
away_teams = [('crd', 'Arizona Cardinals'), ('atl', 'Atlanta Falcons'), 
              ('rav', 'Baltimore Ravens'), ('buf', 'Buffalo Bills'), 
              ('car', 'Carolina Panthers'), ('chi', 'Chicago Bears'), 
              ('cin', 'Cincinnati Bengals'), ('cle', 'Cleveland Browns'), 
              ('dal', 'Dallas Cowboys'), ('den', 'Denver Broncos'), 
              ('det', 'Detroit Lions'), ('gnb', 'Green Bay Packers'), 
              ('htx', 'Houston Texans'), ('clt', 'Indianapolis Colts'), 
              ('jax', 'Jacksonville Jaguars'), ('kan', 'Kansas City Chiefs'), 
              ('rai', 'Las Vegas Raiders'), ('sdg', 'Los Angeles Chargers'), 
              ('ram', 'Los Angeles Rams'), ('mia', 'Miami Dolphins'), 
              ('min', 'Minnesota Vikings'), ('nwe', 'New England Patriots'), 
              ('nor', 'New Orleans Saints'), ('nyg', 'New York Giants'), 
              ('nyj', 'New York Jets'), ('phi', 'Philadelphia Eagles'), 
              ('pit', 'Pittsburgh Steelers'), ('sfo', 'San Francisco 49ers'), 
              ('sea', 'Seattle Seahawks'), ('tam', 'Tampa Bay Buccaneers'), 
              ('oti', 'Tennessee Titans'), ('was', 'Washington Commanders')]  

class TeamForm(FlaskForm):  
    home_team = SelectField('Home Team', choices=home_teams, validators=[DataRequired()]) 
    away_team = SelectField('Away Team', choices=away_teams, validators=[DataRequired()])  
    submit = SubmitField('Get Odds')  

class nTeamForm(FlaskForm):  
    nhome_team = SelectField('Home Team', choices=home_teams, validators=[DataRequired()]) 
    naway_team = SelectField('Away Team', choices=away_teams, validators=[DataRequired()])  

class XpfForm(FlaskForm):
    points = IntegerField('Enter points', validators=[DataRequired(), NumberRange(min=0, max=50)])
    submit = SubmitField('Get Probability')

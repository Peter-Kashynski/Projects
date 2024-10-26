
from flask import Flask, url_for, request, redirect, jsonify, render_template
import pandas as pd   
from functions import get_odds, get_odds_n, pf_at_least, pa_at_least, custom_pf_at_least
from forms import TeamForm, nTeamForm, home_teams, away_teams, XpfForm



app = Flask(__name__)
app.config['SECRET_KEY'] = 'nuh-uh'

@app.route('/') 
def index():  
    return redirect(url_for('odds')) 


@app.route('/odds', methods=['GET', 'POST'])
def odds():    

    custom_xpf = None
    odds = None  
    home_team = None 
    away_team = None 
    winning_prob = None, 
    xpf = None, 
    xpa = None, 
    home_apf = None,
    home_apa = None,
    away_apf = None,
    away_apa = None,  
    home_team_full_name = None, 
    away_team_full_name = None, 
    pf_at_least_5 = None 
    pf_at_least_10 = None
    pf_at_least_15 = None
    pf_at_least_20 = None
    pf_at_least_25 = None
    pf_at_least_30 = None
    pf_at_least_35 = None
    pf_at_least_40 = None
    pf_at_least_45 = None
    pf_at_least_50 = None 
    pa_at_least_5 = None  
    pa_at_least_10 = None 
    pa_at_least_15 = None 
    pa_at_least_20 = None 
    pa_at_least_25 = None 
    pa_at_least_30 = None 
    pa_at_least_35 = None 
    pa_at_least_40 = None 
    pa_at_least_45 = None 
    pa_at_least_50 = None  
    form_submitted = None 
 
    team_dict = dict(home_teams)
    
    form = TeamForm(csrf_enabled=True) 
    xpf_form = XpfForm(csrf_enabled=True)  

    if request.method == 'POST' and form.validate_on_submit():  

        form_submitted = True 
        home_team = form.home_team.data
        away_team = form.away_team.data 

        home_team_full_name = team_dict.get(home_team)
        away_team_full_name = team_dict.get(away_team) 

        pf_prob_list = pf_at_least(home_team, away_team)  

        pf_at_least_5 = pf_prob_list[0]  
        pf_at_least_10 = pf_prob_list[1] 
        pf_at_least_15 = pf_prob_list[2] 
        pf_at_least_20 = pf_prob_list[3] 
        pf_at_least_25 = pf_prob_list[4] 
        pf_at_least_30 = pf_prob_list[5] 
        pf_at_least_35 = pf_prob_list[6] 
        pf_at_least_40 = pf_prob_list[7] 
        pf_at_least_45 = pf_prob_list[8] 
        pf_at_least_50 = pf_prob_list[9]  


        pa_prob_list = pa_at_least(home_team, away_team) 

        pa_at_least_5 = pa_prob_list[0]  
        pa_at_least_10 = pa_prob_list[1] 
        pa_at_least_15 = pa_prob_list[2] 
        pa_at_least_20 = pa_prob_list[3] 
        pa_at_least_25 = pa_prob_list[4] 
        pa_at_least_30 = pa_prob_list[5] 
        pa_at_least_35 = pa_prob_list[6] 
        pa_at_least_40 = pa_prob_list[7] 
        pa_at_least_45 = pa_prob_list[8] 
        pa_at_least_50 = pa_prob_list[9] 
  
        if 'neutral_venue' in request.form:
            odds = get_odds_n(home_team, away_team)
        else:
            odds = get_odds(home_team, away_team)

        winning_prob = odds[0] 
        xpf = odds[1] 
        xpa = odds[2]  
        home_apf = odds[3]
        home_apa = odds[4] 
        away_apf = odds[5] 
        away_apa = odds[6] 

    if xpf_form.validate_on_submit():   
        home_team = form.home_team.data
        away_team = form.away_team.data 
        user_input = xpf_form.points.data
        custom_xpf = custom_pf_at_least(home_team, away_team, user_input) 


    return render_template('odds.html',  
                           form=form,   
                           xpf_form=xpf_form,
                           winning_prob=winning_prob,  
                           xpf=xpf, 
                           xpa=xpa, 
                           home_team=home_team,  
                           away_team=away_team, 
                           home_apf=home_apf,  
                           home_apa=home_apa, 
                           away_apf=away_apf,  
                           away_apa=away_apa, 
                           home_team_full_name=home_team_full_name, 
                           away_team_full_name=away_team_full_name, 
                           pf_at_least_5=pf_at_least_5,  
                           pf_at_least_10=pf_at_least_10, 
                           pf_at_least_15=pf_at_least_15,
                           pf_at_least_20=pf_at_least_20,
                           pf_at_least_25=pf_at_least_25,
                           pf_at_least_30=pf_at_least_30,
                           pf_at_least_35=pf_at_least_35,
                           pf_at_least_40=pf_at_least_40,
                           pf_at_least_45=pf_at_least_45,
                           pf_at_least_50=pf_at_least_50, 
                           pa_at_least_5=pa_at_least_5,  
                           pa_at_least_10=pa_at_least_10, 
                           pa_at_least_15=pa_at_least_15,
                           pa_at_least_20=pa_at_least_20,
                           pa_at_least_25=pa_at_least_25,
                           pa_at_least_30=pa_at_least_30,
                           pa_at_least_35=pa_at_least_35,
                           pa_at_least_40=pa_at_least_40,
                           pa_at_least_45=pa_at_least_45,
                           pa_at_least_50=pa_at_least_50, 
                           form_submitted=form_submitted, 
                           custom_xpf=custom_xpf
                           )

@app.route('/about') 
def about():  
    return render_template('about.html')
    


if __name__ == '__main__':
    app.run(debug=True)


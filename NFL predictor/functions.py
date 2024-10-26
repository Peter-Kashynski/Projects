import pandas as pd 
import requests  
import numpy as np 
import matplotlib.pyplot as plt 
from sklearn.linear_model import LogisticRegression  
from sklearn.linear_model import LinearRegression   
import warnings 
from sklearn.exceptions import DataConversionWarning  
from sklearn.model_selection import train_test_split  
from scipy.stats import norm

ndf = pd.read_csv(r"C:\Users\tak86\OneDrive\Desktop\ML algorithms\completeDF.csv") 

NX = ndf[['XPF', 'XPA']]  
Ny = ndf['Result']  

NX_train, NX_test, Ny_train, Ny_test = train_test_split(NX, Ny, train_size=0.8, random_state = 14)

Nmodel = LogisticRegression() 
Nmodel.fit(NX_train, Ny_train) 

Nscore = Nmodel.score(NX_test, Ny_test)  


df = pd.read_csv(r"C:\Users\tak86\OneDrive\Desktop\ML algorithms\venueDataframe.csv")

X = df[['XPF', 'XPA']] 
y = df['Result'] 

predict_winner = LogisticRegression() 

X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=0.8, random_state=23) 

predict_winner.fit(X_train, y_train) 





# n for neutral 
def npf_prediction(avg_pf, opp_avg_pa):   
    ''' using the model's coefficients to return the xpf '''
    predicted_pf = ((-0.37122471 * avg_pf) + (-0.25217794 * opp_avg_pa) +   
                   (0.06270447 * (avg_pf * opp_avg_pa)) + 5.463637586537391)
    return predicted_pf  

def npa_prediction(avg_pa, opp_avg_pf):   
    ''' using the model's coefficients to return the xpa ''' 
    predicted_pa = ((-0.14014459 * avg_pa) + (-0.10277674 * opp_avg_pf) +  
                    (0.0490133 * (avg_pa * opp_avg_pf)) + 3.6171709008903825) 
    return predicted_pa   

# predictors for venue-influenced games 
def pf_prediction(avg_pf, opp_avg_pa, venue):    
    ''' using the model's coefficients to return the xpf ''' 
    predicted_pf = ((-0.6491474 * avg_pf) + (-0.73558525 * opp_avg_pa) +   
                   (0.07833492 * (avg_pf * opp_avg_pa)) +  
                   (venue * 2.55008384) + 13.430173738279173)  
    return predicted_pf 

def pa_prediction(avg_pa, opp_avg_pf, venue):   
    ''' using the model's coefficients to return the xpa ''' 
    predicted_pa = ((-0.43913402 * avg_pa) + (-0.47575419 * opp_avg_pf) +  
                    (0.0655604 * (avg_pa * opp_avg_pf)) +  
                    (venue * -2.57068664) + 11.634025975279709) 
    return predicted_pa  


# c for complete 
cdf = pd.read_csv(r"C:\Users\tak86\OneDrive\Desktop\ML algorithms\completeDF.csv") 

from sklearn.preprocessing import OrdinalEncoder 
result = ['L', 'W'] 
enc = OrdinalEncoder(categories = [result]) 
cdf['Result'] = enc.fit_transform(cdf[['Result']]) 

warnings.filterwarnings(action='ignore', category=UserWarning, module='sklearn') 

def get_odds(your_team, opponent):  
    
    your_rows = df[df['Team'] == your_team]   
    your_row = your_rows.iloc[0] 

    opponent_rows = df[df['Team'] == opponent]  
    opponent_row = opponent_rows.iloc[0] 

    your_apf = round(your_row['Avg_PF'].item(), 2) 
    your_apa = round(your_row['Avg_PA'].item(), 2)

    opponent_apf = round(opponent_row['Avg_PF'].item(), 2)
    opponent_apa = round(opponent_row['Avg_PA'].item(), 2)

    pf_pred = round(pf_prediction(your_apf, opponent_apa, 1), 2)
    pa_pred = round(pa_prediction(your_apa, opponent_apf, 1), 2)  

    new_value = np.array([[pf_pred, pa_pred]])    
    new_input = pd.DataFrame(new_value, columns=['XPF', 'XPA']) 

    probability = predict_winner.predict_proba(new_input)
    winning_prob = (float(probability[0][1])) * 100  
    winning_prob = round(winning_prob, 1)

    xpf = pf_pred
    xpa = pa_pred

    return winning_prob, xpf, xpa, your_apf, your_apa, opponent_apf, opponent_apa
# print(get_odds('dal', 'nyg')) 


def get_odds_n(your_team, opponent):
    
    your_rows = df[df['Team'] == your_team]   
    your_row = your_rows.iloc[0] 

    opponent_rows = df[df['Team'] == opponent]  
    opponent_row = opponent_rows.iloc[0] 

    your_apf = round(your_row['Avg_PF'].item(), 2) 
    your_apa = round(your_row['Avg_PA'].item(), 2)

    opponent_apf = round(opponent_row['Avg_PF'].item(), 2)
    opponent_apa = round(opponent_row['Avg_PA'].item(), 2)

    pf_pred = round(npf_prediction(your_apf, opponent_apa), 2)
    pa_pred = round(npa_prediction(your_apa, opponent_apf), 2) 

    new_value = np.array([[pf_pred, pa_pred]])    
    new_input = pd.DataFrame(new_value, columns=['XPF', 'XPA']) 

    probability = Nmodel.predict_proba(new_input)
    winning_prob = round(float(probability[0][1]), 2)    

    xpf = pf_pred
    xpa = pa_pred

    return winning_prob, xpf, xpa, your_apf, your_apa, opponent_apf, opponent_apa
# print(get_odds_n('dal', 'nyg'))


def pf_at_least(your_team, opponent): 
    winning_prob, xpf, xpa, your_apf, your_apa, opponent_apf, opponent_apa = get_odds(your_team, opponent)   

    predicted_pf = xpf
    target_score = range(5, 51, 5) 
    target_score_list = []
    for score in target_score:
        target_score_list.append(score)

    sigma = 12  
    pf_prob_list = []
    for score in target_score_list:
        z_score = (score - predicted_pf) / sigma
        prob = round(1 - norm.cdf(z_score).item(), 2) 
        pf_prob_list.append(prob) 

    # score_prob_list = list(zip(target_score_list, prob_list)) 
    pf_prob_list = list(pf_prob_list)  
    pf_prob_list = [int(round(prob * 100, 2)) for prob in pf_prob_list]
    return pf_prob_list
#print(pf_at_least('dal', 'nyg')) 

def pa_at_least(your_team, opponent): 
    winning_prob, xpf, xpa, your_apf, your_apa, opponent_apf, opponent_apa = get_odds(your_team, opponent)   

    predicted_pa = xpa
    target_score = range(5, 51, 5) 
    target_score_list = []
    for score in target_score:
        target_score_list.append(score)

    sigma = 12  
    pa_prob_list = []
    for score in target_score_list:
        z_score = (score - predicted_pa) / sigma
        prob = round(1 - norm.cdf(z_score).item(), 2) 
        pa_prob_list.append(prob) 

    pa_prob_list = list(pa_prob_list)  
    pa_prob_list = [int(round(prob * 100, 2)) for prob in pa_prob_list]
    return pa_prob_list 
#print(pa_at_least('dal', 'nyg'))  


def custom_pf_at_least(your_team, opponent, points): 
    
    result = get_odds(your_team, opponent)  
    xpf = result[1] 

    sigma = 12  
    z_score = (points - xpf) / sigma
    prob = 1 - norm.cdf(z_score)  
    prob = round(prob, 2) # type: ignore

    return prob  


# result = custom_pf_at_least('dal', 'nyg', 30) 
# print(result)











# -*- coding: utf-8 -*-
"""
Created on Sun Sep 15 17:04:45 2019

@author: ichch
"""

from selenium import webdriver
import sys
import time
import pandas as pd
import numpy as np
def generate_win_matrix(tbl):
    team_result_df = None
    
    for key in tbl:
        team_df = pd.DataFrame(eval(tbl[key]))
        for entry in team_df.iterrows():
            temp_dict = {}
            entry = entry[1]
            temp_dict['Team A'] = entry['teama_short_name']
            temp_dict['Team B'] = entry['teamb_short_name']
            temp_dict['Goal'] = '{}-{}'.format(entry['teama_score'],entry['teamb_score'])
            temp_dict['id'] = entry['id']
            if entry['result'] == 'L':
                if key == entry['teamb_short_name']:
                    temp_dict['Winner'] = entry['teama_short_name']
                else:
                    temp_dict['Winner'] = entry['teamb_short_name']
            elif entry['result'] == 'W':
                if key == entry['teamb_short_name']:
                    temp_dict['Winner'] = entry['teamb_short_name']
                else:
                    temp_dict['Winner'] = entry['teama_short_name']
            else:
                temp_dict['Winner'] = 'tie'
            
            if team_result_df is None:
                team_result_df = pd.DataFrame([temp_dict])
            else : 
                team_result_df = team_result_df.append(pd.DataFrame([temp_dict]))
    team_result_df.drop_duplicates(subset='id',inplace=True)
    team_result_df.set_index('id',inplace=True)
    return team_result_df
if __name__ == "__main__":   
    for season in range(1,8):
        tbl_season = pd.read_csv("Season {}_standings.csv".format(season))
        win_matrix = generate_win_matrix(dict(zip(tbl_season['team_short_name'],tbl_season['match_result'])))
        win_matrix.to_csv("Season {}_wins_lose.csv".format(season),index=None)
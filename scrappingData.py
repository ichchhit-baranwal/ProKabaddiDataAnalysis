# -*- coding: utf-8 -*-
"""
Created on Sun Sep 15 17:04:45 2019

@author: ichch
"""

from selenium import webdriver
import sys
import time
from bs4 import BeautifulSoup
import pandas as pd
import json
import requests
from multiprocessing import Pool

def extract_data(params):
    r = requests.get(params[1])
    json_dict = json.loads(r.content)
    stat_data_frame = pd.DataFrame(json_dict['data'])
    stat_data_frame['stat'] = json_dict['stat']
    stat_data_frame['season'] = params[0]
    if 'player' in json_dict['data'][0]:
        stat_data_frame.drop('player',axis='columns',inplace=True)
    if 'match played' in json_dict['data'][0]:
        stat_data_frame.drop('match played',axis='columns',inplace=True)
    if 'team' in json_dict['data'][0]:
        stat_data_frame.drop('team',axis='columns',inplace=True)
    return stat_data_frame

if __name__ == "__main__":   
    options = webdriver.ChromeOptions()
    options.add_argument('-headless')
    options.add_argument('-no-sandbox')
    options.add_argument('-disable-dev-shm-usage')
    wd = webdriver.Chrome('C:\\Users\\ichch\\Downloads\\chromedriver_win32\\chromedriver',options=options)
    json_pre_url = "https://www.prokabaddi.com/sifeeds/kabaddi/static/json/1_{series_id}_{stat_id}_stats.json"
    wd.get('https://www.prokabaddi.com/stats/1-96-total-points-statistics')
    time.sleep(3)
    soup = BeautifulSoup(wd.page_source,"lxml")
    season_element = soup.select("#season_dropdown")
    tmp_lst = season_element[0].find_all(recursive=False)
    
    series_ids = dict((x['data-series-id'],x.decode_contents()) for x in tmp_lst)
    print(series_ids)
    
    wd.find_element_by_id('player_Btn').click()
    time.sleep(3)
    soup = BeautifulSoup(wd.page_source,"lxml")
    player_stats_elem = soup.select('#si_dropdown')
    tmp_lst = player_stats_elem[0].find_all(recursive=False)
    player_stat_ids = dict((x['data-stat-id'],x.decode_contents()) for x in tmp_lst)
    print(player_stat_ids)
    
    wd.find_element_by_id('team_Btn').click()
    time.sleep(3)
    soup = BeautifulSoup(wd.page_source,"lxml")
    team_stats_elem = soup.select('#si_dropdown')
    tmp_lst = team_stats_elem[0].find_all(recursive=False)
    team_stat_ids = dict((x['data-stat-id'],x.decode_contents()) for x in tmp_lst)
    print(team_stat_ids)
	
	
    #params_team = [(series_ids[series_id],json_pre_url.format(series_id=series_id,stat_id=stat_id)) for series_id in series_ids for stat_id in team_stat_ids]
    params_player = [(series_ids[series_id],json_pre_url.format(series_id=series_id,stat_id=stat_id)) for series_id in series_ids for stat_id in player_stat_ids]
    
	
	
    #pool = Pool()
    #team_dfs = pool.map(extract_data,params_team)
    #pool.close()
    #pool.join()


    pool = Pool()
    player_dfs = pool.map(extract_data,params_player)
    pool.close()
    pool.join()
	
	
	
    #team_data_frame = None
    #for df in team_dfs:
    #    if team_data_frame is None:
    #        team_data_frame=df
    #    else:
    #        team_data_frame = team_data_frame.append(df)
    #team_data_frame.to_csv("team_stats.csv",index=False)
	
    player_data_frame = None
    for df in player_dfs:
        if player_data_frame is None:
            player_data_frame=df
        else:
            player_data_frame = player_data_frame.append(df)
    print(player_data_frame)
    player_data_frame.to_csv("player_stats.csv",index=False)
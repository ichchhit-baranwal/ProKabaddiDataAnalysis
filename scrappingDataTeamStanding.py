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
    stat_data_frame = None
    for group in json_dict['standings']['groups']:
        for team in group['teams']['team']:
            if stat_data_frame is None:
                stat_data_frame = pd.DataFrame(team,index=None)
            else:
                stat_data_frame = stat_data_frame.append(pd.DataFrame(team,index=None))
    stat_data_frame['season'] = params[0]
    stat_data_frame = stat_data_frame.reset_index()
    stat_data_frame.drop(columns=['team_global_id','index','ga','gf'],inplace=True)
    return stat_data_frame

if __name__ == "__main__":   
    options = webdriver.ChromeOptions()
    options.add_argument('-headless')
    options.add_argument('-no-sandbox')
    options.add_argument('-disable-dev-shm-usage')
    wd = webdriver.Chrome('C:\\Users\\ichch\\Downloads\\chromedriver_win32\\chromedriver',options=options)
    json_pre_url = "https://www.prokabaddi.com/sifeeds/kabaddi/live/json/{series_id}_standing.json"
    wd.get('https://www.prokabaddi.com/stats/1-96-total-points-statistics')
    time.sleep(3)
    soup = BeautifulSoup(wd.page_source,"lxml")
    season_element = soup.select("#season_dropdown")
    tmp_lst = season_element[0].find_all(recursive=False)
    
    series_ids = dict((x['data-series-id'],x.decode_contents()) for x in tmp_lst)
    series_ids.pop('0')
    print(series_ids)
    params_team = [(series_ids[series_id],json_pre_url.format(series_id=series_id)) for series_id in series_ids]
    pool = Pool(1)
    team_dfs = pool.map(extract_data,params_team)
    pool.close()
    pool.join()
    team_data_frame = None
    # for df in team_dfs:
        # if team_data_frame is None:
            # team_data_frame=df
        # else:
            # team_data_frame = team_data_frame.append(df)
    #team_data_frame.to_csv("team_stats.csv",index=False)
    for team in team_dfs:
        # print(team['season'][0])
        team.to_csv("{}_standings.csv".format(team['season'][0]),index=False)
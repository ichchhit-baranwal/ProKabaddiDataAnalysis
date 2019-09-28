import pandas as pd
tbl = pd.read_csv('team_stats.csv')
tbl = tbl[~(tbl.season=='All Seasons')]
for season in tbl.season.unique():
    tbl_season = tbl[tbl.season==season]
    team_dict = dict(dict(tuple(tbl_season.groupby(['team_id','team_name']))).keys())
    tbl_new = tbl_season.pivot(index='team_id',columns='stat',values='value').reset_index()
    
    tbl_new['team_name'] = [team_dict[team_id] for team_id in tbl_new.team_id]
    tbl_new.to_csv("{}_team_stats.csv".format(season),index=None)
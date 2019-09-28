import pandas as pd
tbl = pd.read_csv('player_stats.csv')
tbl = tbl[~(tbl.season=='All Seasons')]
for season in tbl.season.unique():
    tbl_season = tbl[tbl.season==season]
    player_name_dict = dict(dict(tuple(tbl_season.groupby(['player_id','player_name']))).keys())
    player_team_dict = dict(dict(tuple(tbl_season.groupby(['player_id','team_id']))).keys())
    player_position_dict = dict(dict(tuple(tbl_season.groupby(['player_id','position_id']))).keys())
    player_posname_dict = dict(dict(tuple(tbl_season.groupby(['player_id','position_name']))).keys())
    player_match_dict = dict(dict(tuple(tbl_season.groupby(['player_id','match_played']))).keys())
    tbl_new = tbl_season.pivot(index='player_id',columns='stat',values='value').reset_index()
    # print(player_position_dict)
    try:
        tbl_new['player_name'] = [player_name_dict[player_id] if player_id in player_position_dict.keys() else None for player_id in tbl_new.player_id]
        tbl_new['team'] = [player_team_dict[player_id] if player_id in player_position_dict.keys() else None for player_id in tbl_new.player_id]
        tbl_new['position_id'] = [player_position_dict[player_id] if player_id in player_position_dict.keys() else None for player_id in tbl_new.player_id]
        tbl_new['position_name'] = [player_posname_dict[player_id] if player_id in player_position_dict.keys() else None for player_id in tbl_new.player_id]
        tbl_new['match_played'] = [player_match_dict[player_id] if player_id in player_position_dict.keys() else None for player_id in tbl_new.player_id]
    except Exception as ex:
        print("season",season,ex)
    tbl_new.to_csv("{}_player_stats.csv".format(season),index=None)
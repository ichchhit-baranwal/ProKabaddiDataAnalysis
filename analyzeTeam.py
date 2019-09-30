import numpy as np
import pandas as pd
# import seaborn as sb
import matplotlib.pyplot as plt
# from sklearn.decomposition import PCA
from sklearn.naive_bayes import GaussianNB
from sklearn import linear_model
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import PolynomialFeatures
def analyze_team_stats_season(season):
    tbl = pd.read_csv("Season {}_team_stats.csv".format(season))
    tbl_standing = pd.read_csv("Season {}_standings.csv".format(season))
    

    column_to_consider = [tbl.columns[0]]
    column_to_consider.extend(columns_to_use)
    # scaled_tbl = pd.DataFrame(StandardScaler().fit_transform(tbl[tbl.columns[1:-1]]),columns = tbl.columns[1:-1])
    # scaled_tbl[tbl.columns[0]]=tbl[tbl.columns[0]]
    tbl = tbl[column_to_consider]
    
    joined_tbl = tbl.merge(tbl_standing[['team_id','team_name','points','wins']],on="team_id",how='inner')
    return joined_tbl
    # cols = [param for param in tbl.columns[2:]]
    # corr = tbl[cols].corr()
    # plt.matshow(corr)
    # plt.xticks(range(len(cols)),cols,rotation=90)
    # plt.yticks(range(len(cols)),cols)
    # cb = plt.colorbar()
    # cb.ax.tick_params(labelsize=14)

def classify_and_predict(training_tbl):
    X_poly = poly.fit_transform(training_tbl[columns_to_use])
    poly.fit(X_poly,training_tbl['points'])
    model = linear_model.LinearRegression()
    model.fit(X_poly,training_tbl['points'])
    return model
    
if __name__ == "__main__":
    train_data_frame = None
    # columns_to_use = ['Team All-outs Conceded','Team DOD Raid Points','Team Successful Raids',\
    # 'Team Successful Tackles','Team Super Raid','Team Super Tackles']
    columns_to_use = ['Team Average Raid Points','Team Average Tackle Points','Team Avg Points Scored']
    poly = PolynomialFeatures(degree=1)
    for season in range(1,6):
        tbl = analyze_team_stats_season(season)
        if train_data_frame is None:
            train_data_frame = tbl
        else:
            train_data_frame.append(tbl)
    test_Val = analyze_team_stats_season(7)
    # columns_to_use.append("wins")
    model = classify_and_predict(train_data_frame)
    
    
    y_vals = model.predict(poly.fit_transform(test_Val[columns_to_use]))
    print([int(val) for val in y_vals])
    print(test_Val['points'].tolist())
    print(test_Val['team_name'].tolist())
    # plt.show()
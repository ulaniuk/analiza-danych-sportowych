import pandas as pd
import plotly.express as px

from datetime import datetime
from meteostat import Point, Daily


# Stadiums locations
stadium_location = {
    "Wigan Athletic": Point(53.087216437622686, -2.4333814565533727, 0),
    "Burton Albion": Point(53.087216437622686, -2.4333814565533727, 0),
    "Crewe Alexandra": Point(53.087216437622686, -2.4333814565533727, 0),
    "Wycombe Wanderers": Point(53.087216437622686, -2.4333814565533727, 0),
}

# Stadiums capacity
stadium_capacity = {
    "Wigan Athletic": 25_138, 
    "Burton Albion": 6_912,
    "Crewe Alexandra": 10_153,
    "Wycombe Wanderers": 9_558,
}

def get_temperature(location, date):
    date = datetime.strptime(date, '%Y-%m-%d')

    return Daily(location, date, date).fetch()['tavg'][0]

def get_wind_speed(location, date):
    date = datetime.strptime(date, '%Y-%m-%d')

    return Daily(location, date, date).fetch()['wspd'][0]

def remove_penalties(string):
    if '(' in  str(string):
        return int(string[:-3])
    return int(string)

def get_win_streak(data, record):
    # Returns length of winning streak for current match

    record_index = record.name
    streak = 0

    for i in range(record_index-1, 0, -1):
        if data.iloc[[i]]['Result'].values[0] == 'W':
            streak += 1
        else:
            break

    return streak

def get_not_lose_streak(data, record):
    # Returns length of not losing streak for current match

    record_index = record.name
    streak = 0

    for i in range(record_index-1, 0, -1):
        if data.iloc[[i]]['Result'].values[0] == 'W' or data.iloc[[i]]['Result'].values[0] == 'D':
            streak += 1
        else:
            break

    return streak

def get_last_five_games_goals_for(data, record):
    # Returns number of scored goals in last 5 matches

    record_index = record.name
    scored_goals = 0

    for i in range(record_index-1, record_index-6, -1):
        if i < 0:
            break

        scored_goals += data.iloc[[i]]['GF'].values[0]

    return scored_goals

def get_last_five_games_goals_against(data, record):
    # Returns number of scored goals in last 5 matches

    record_index = record.name
    scored_goals = 0

    for i in range(record_index-1, record_index-6, -1):
        if i < 0:
            break

        scored_goals += data.iloc[[i]]['GA'].values[0]

    return scored_goals

def get_oponent_position():
    # gets league table position of an oponent TODO: implement
    pass



df_wigan = pd.read_csv("wigan.csv")
df_albion = pd.read_csv("albion.csv")
df_alexandra = pd.read_csv("alexandra.csv")
df_wycombe = pd.read_csv("wycombe.csv")

df_wigan["Club"] = "Wigan Athletic"
df_albion["Club"] = "Burton Albion"
df_alexandra["Club"] = "Crewe Alexandra"
df_wycombe["Club"] = "Wycombe Wanderers"

for df in [df_wigan, df_albion, df_alexandra, df_wycombe]:
    location_point = stadium_location[df['Club'].values[0]]
    capacity = stadium_capacity[df['Club'].values[0]]

    df['Attendance percentage'] = df['Attendance'].apply(lambda x: x/capacity)

    df['Temperature'] = df['Date'].apply(lambda x: get_temperature(location_point, x))
    df['Wind'] = df['Date'].apply(lambda x: get_wind_speed(location_point, x))

    df['GA'] = df['GA'].apply(lambda x: remove_penalties(x))
    df['GF'] = df['GF'].apply(lambda x: remove_penalties(x))

    df['Win streak'] = df.apply(lambda x: get_win_streak(df, x), axis=1)
    df['Not lose streak'] = df.apply(lambda x: get_not_lose_streak(df, x), axis=1)

    df['Last 5 games goals for'] = df.apply(lambda x: get_last_five_games_goals_for(df, x), axis=1)
    df['Last 5 games goals against'] = df.apply(lambda x: get_last_five_games_goals_against(df, x), axis=1)


df = pd.concat([df_wigan, df_wycombe, df_albion, df_alexandra])

df.to_csv('data.csv', index=False)

df = df[df["Venue"] == "Home"]
# df = df[(df["Day"] == "Sat") | (df["Day"] == "Tue")]
print(df.groupby(by=["Day"]).mean())


fig = px.histogram(df, x="Club", y="Attendance", color='Comp', barmode='group', histfunc='avg')
fig.update_layout(title_text="Tournaments attendance", title_x=0.5, yaxis_title="Average attendance")
fig.show()

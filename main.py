import pandas as pd
import plotly.express as px


df_wigan = pd.read_csv("wigan.csv")
df_albion = pd.read_csv("albion.csv")
df_alexandra = pd.read_csv("alexandra.csv")
df_wycombe = pd.read_csv("wycombe.csv")


df_wigan["Club"] = "Wigan Athletic"
df_albion["Club"] = "Burton Albion"
df_alexandra["Club"] = "Crewe Alexandra"
df_wycombe["Club"] = "Wycombe Wanderers"

df = pd.concat([df_wigan, df_wycombe, df_albion, df_alexandra])
df = df[df["Venue"] == "Home"]
# df = df[(df["Day"] == "Sat") | (df["Day"] == "Tue")]
print(df.groupby(by=["Day"]).mean())


fig = px.histogram(df, x="Club", y="Attendance", color='Comp', barmode='group', histfunc='avg')
fig.update_layout(title_text="Tournaments attendance", title_x=0.5, yaxis_title="Average attendance")
fig.show()

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import base64
import seaborn as sns


@st.cache_data
def load_data(year):
    url = "https://www.basketball-reference.com/leagues/NBA_" + str(year) + "_per_game.html"
    html = pd.read_html(url, header=0)
    scrapped_df = html[0]
    raw = scrapped_df.drop(scrapped_df[scrapped_df['Age'] == 'Age'].index).fillna(0)
    player_data = raw.drop(['Rk'], axis=1)

    return player_data


def file_download(base_df):
    csv = base_df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # strings to bits conversion
    href = f'<a href="data:file/csv;base64,{b64}" download=player_stats.csv> Download CSV File</a>'
    return href


# app title
st.title('NBA Player Stats Explorer')

# data source
st.markdown("""
**Data source**: [Basketball-reference.com](https://www.basketball-reference.com/)
""")

# sidebar to select year, team, position
st.sidebar.header('User Input Features')
selected_year = st.sidebar.selectbox('Year', list(reversed(range(1950, 2024))))

player_stats = load_data(selected_year)

unique_team = sorted(player_stats['Team'].unique()[:-1])
selected_team = st.sidebar.multiselect('Player Team', unique_team, unique_team)

unique_pos = player_stats['Pos'].unique()[:-1]
selected_pos = st.sidebar.multiselect('Position', unique_pos)

# filtering data
df_selected_team = player_stats[(player_stats['Team'].isin(selected_team)) & (player_stats['Pos'].isin(selected_pos))]

st.header('Display Player Stats of Selected Team(s)')
st.write('Data dimension: ' + str(df_selected_team.shape[0]) + 'rows and ' + str(df_selected_team.shape[1]) + ' columns')
st.dataframe(df_selected_team)

# download CSV file link
st.markdown(file_download(df_selected_team), unsafe_allow_html=True)

# heatmap
if st.button('Intercorrelation Heatmap'):
    st.header('Intercorrelation Matrix Heatmap')
    df_heatmap = df_selected_team.drop(columns=['Player', 'Team', 'Pos', 'Awards'])
    df_heatmap.to_csv('output.csv', index=False)
    df = pd.read_csv('output.csv')

    corr = df.corr()
    mask = np.zeros_like(corr)
    mask[np.triu_indices_from(mask)] = True
    with sns.axes_style("white"):
        f, ax = plt.subplots(figsize=(7, 5))
        ax = sns.heatmap(corr, mask=mask, vmax=1, square=True)
    st.pyplot(f)

# bar chart
if st.button('Barchart for triples'):
    st.header('Barchart teams and triples')
    df_selected_team.to_csv('output.csv', index=False)
    df = pd.read_csv('output.csv')

    with sns.axes_style("white"):
        f, ax = plt.subplots(figsize=(15, 5))
        ax = sns.barplot(x='Team', y='3P', data=df)

    st.pyplot(f)

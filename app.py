import streamlit as st
import pandas as pd
from streamlit_autorefresh import st_autorefresh
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

st.set_page_config(
    page_title="SIUUUUUU",
    page_icon="🐐"
    )

col1, col2 = st.columns([6,1])
with col1:
    st.title("🐐 PL Predictions SIUUUUU")
with col2:
    st.image('siuuu.gif')

if 'kzscore' not in st.session_state:
    st.session_state['kzscore'] = 0
if 'yyscore' not in st.session_state:
    st.session_state['yyscore'] = 0

#Table to keep track of scores
score_table = pd.DataFrame([{
    'KZ': st.session_state.kzscore,
    'YY': st.session_state.yyscore
}])

if st.button('Click to watch my score go up!!! SIIUUUUUU'):
    st.session_state.kzscore += 1
    st.rerun()

# Display score table
score_table = score_table.T
score_table.columns = ['Score']
score_table = score_table.sort_values(by = 'Score', ascending=False)
st.table(score_table)

# Get match details from fpl api
base_url = 'https://fantasy.premierleague.com/api/'

fixture_list = requests.get(base_url+'fixtures/').json()
main = requests.get(base_url+'bootstrap-static/').json()

fixtures = pd.json_normalize(fixture_list)

teams = pd.json_normalize(main['teams'])

# Merge team name to fixtures table
teams_names = teams[['id', 'name', 'short_name']]
teams_names = teams_names.rename(columns = {'id':'team_id'})

teams_away = teams_names.add_suffix('_away')
teams_home = teams_names.add_suffix('_home')

fixtures = fixtures.merge(teams_away, left_on='team_a', right_on='team_id_away')
fixtures = fixtures.merge(teams_home, left_on='team_h', right_on='team_id_home')

fixtures = fixtures.rename(columns={'event':'gameweek'})

# Get relevant columns
matches = fixtures[['gameweek', 'kickoff_time', 'finished', 'team_h_score', 'team_a_score', 'name_home', 'short_name_home', 'name_away', 'short_name_away']]
# Convert kickoff_time to datetime
matches.loc[:, 'kickoff_time'] = pd.to_datetime(matches['kickoff_time'], format = '%Y-%m-%dT%H:%M:%SZ')

gw = matches[matches['gameweek']==23]['kickoff_time'].min()
#st.table(matches)
now = datetime.now()
st.write(now+timedelta(hours=8))

st_autorefresh(interval=10000, key="autorefresh")
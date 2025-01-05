import streamlit as st
import pandas as pd
from mplsoccer import Sbopen, VerticalPitch
import matplotlib.pyplot as plt
import warnings
import google.generativeai as genai
import utils.helpers as hp


warnings.filterwarnings('ignore')
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
parser = Sbopen(dataframe=True)

st.write("""
# Match Analysis

Choose the competition name, season, home team, and away team and the desired plot. Plots will be shown for both teams and a short description will be created below them.\n
Some datasets are not supported due to differences in data but most recent competitions should work.
""")

@st.cache_data
def load_competition_data():
    return parser.competition()

@st.cache_data
def load_matches(competition_id, season_id):
    return parser.match(competition_id, season_id)

try:
    competition = load_competition_data()
    competition_name = st.selectbox("Select Competition:", competition['competition_name'].unique())

    seasons = competition[competition['competition_name'] == competition_name]
    selected_season = st.selectbox("Select Season:", seasons['season_name'].unique())

    exact_season = seasons[seasons['season_name'] == selected_season]
    competition_id = exact_season['competition_id'].iloc[0]
    season_id = exact_season['season_id'].iloc[0]

    matches = load_matches(competition_id, season_id)

    team1 = st.selectbox("Select Home Team:", matches['home_team_name'].unique())

    team2_options = [team for team in matches['away_team_name'].unique() if team != team1]
    team2 = st.selectbox("Select Away Team:", team2_options)

    plot_type = st.selectbox("Select Plot Type:", ["Passes/Assists", "Shots/Goals"])

    home_team = team1
    away_team = team2

    st.write(f"Match: {home_team} (Home) vs {away_team} (Away)")
    st.write(f"Competition: {competition_name}, Season: {selected_season}")

    match_data = matches[
        (matches['home_team_name'] == home_team) & (matches['away_team_name'] == away_team)
    ]

    if not match_data.empty:
        match_id = match_data['match_id'].iloc[0]
        st.write("Match found!")
        st.write(f"Match ID: {match_id}")
        st.write(match_data)

        match_details = match_data.loc[match_data['match_id'] == match_id, 
                                    ['home_score', 'away_score', 
                                     'home_team_managers_nickname', 
                                     'away_team_managers_nickname', 
                                     'stadium_name']]
        
        if not match_details.empty:
            home_score = match_details['home_score'].iloc[0]
            away_score = match_details['away_score'].iloc[0]
            home_manager = match_details['home_team_managers_nickname'].iloc[0]
            away_manager = match_details['away_team_managers_nickname'].iloc[0]
            stadium_name = match_details['stadium_name'].iloc[0]

        df_event, df_related, df_freeze, df_tactics = parser.event(match_id)

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 7))
        pitch = VerticalPitch(line_color="black", half=True)

        for team, ax in [(team1, ax1), (team2, ax2)]:
            pitch.draw(ax=ax)

            df = df_event[df_event["team_name"] == team]

            if plot_type == "Passes/Assists":
                df1 = df[df["type_name"] == "Pass"]
                df1 = df1[~df1["outcome_name"].isin(["Incomplete", "Out", "Unknown", "Pass Offside"])]

                filtered_df = df1[(df1["end_y"] > 18) & (df1["end_y"] < 62) & (df1["end_x"] > 102)]
                df_assists = filtered_df[filtered_df["pass_goal_assist"] == True]

                pitch.arrows(filtered_df["x"], filtered_df["y"],
                            filtered_df["end_x"], filtered_df["end_y"],
                            color="red", ax=ax, width=2, headwidth=5, headlength=5, alpha=0.8)

                pitch.scatter(df_assists["x"], df_assists["y"],
                            color="green", s=50, ax=ax, alpha=1.0, edgecolor="black")

                ax.set_title(f"{team} - Passes and Assists into the box")

            elif plot_type == "Shots/Goals":
                df2 = df[df["type_name"] == "Shot"]
                df_goals = df2[df2["outcome_name"] == 'Goal']

                pitch.scatter(df2["x"], df2["y"],
                            color="red", s=50, ax=ax, alpha=0.7, edgecolor="black", label="Shots")

                pitch.scatter(df_goals["x"], df_goals["y"],
                            color="green", s=50, ax=ax, alpha=1.0, edgecolor="black", label="Goals")

                ax.set_title(f"{team} - Shots and Goals")

        plt.tight_layout()
        st.pyplot(fig)

        ai_interpretation = hp.get_ai_interpretation(plot_type, team1, team2, df_event, home_score, away_score, home_manager, away_manager, stadium_name)
        st.write(f"{team1} {home_score}:{away_score} {team2}")
        st.write(ai_interpretation)

    else:
        st.write("No match found for the selected teams in this competition and season.")

except Exception as e:
    st.error(f"An error occurred: {str(e)}. Try another match or competition.")

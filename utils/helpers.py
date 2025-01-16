import streamlit as st
import google.generativeai as genai

def get_ai_interpretation(plot_type, team, opponent, df,home_score, away_score, home_manager, away_manager, stadium_name):
    model = genai.GenerativeModel(st.secrets["GEMINI_CHAT_MODEL"])
    
    if plot_type == "Passes/Assists":
        df1 = df[df["team_name"] == team]

        total_shots = len(df1[df1["type_name"] == "Shot"])
        total_passes = len(df1[df1["type_name"] == "Pass"])
        successful_passes = len(df1[(df["type_name"] == "Pass") & (~df1["outcome_name"].isin(["Incomplete", "Out", "Unknown", "Pass Offside"]))])
        passes_into_box = len(df1[(df1["type_name"] == "Pass") & (df1["end_y"] > 18) & (df1["end_y"] < 62) & (df1["end_x"] > 102)])
        assists = len(df1[(df1["type_name"] == "Pass") & (df1["pass_goal_assist"] == True)])

        df2 = df[df["team_name"] == opponent]

        total_shots2 = len(df2[df2["type_name"] == "Shot"])
        total_passes2 = len(df2[df2["type_name"] == "Pass"])
        successful_passes2 = len(df2[(df2["type_name"] == "Pass") & (~df2["outcome_name"].isin(["Incomplete", "Out", "Unknown", "Pass Offside"]))])
        passes_into_box2 = len(df2[(df2["type_name"] == "Pass") & (df2["end_y"] > 18) & (df2["end_y"] < 62) & (df2["end_x"] > 102)])
        assists2 = len(df2[(df2["type_name"] == "Pass") & (df2["pass_goal_assist"] == True)])
        
        prompt = f"""You are a football analyst who needs to give his insights into the following match data information for {team} against {opponent}:
        Total passes: {total_passes}
        Successful passes: {successful_passes}
        Passes into the box: {passes_into_box}
        Assists: {assists}
        Total shots: {total_shots}
        Goals: {home_score}
        Opponents goals: {away_score}
        Home manager name: {home_manager}
        Away manager name: {away_manager}
        Stadium name: {stadium_name}
        Total shots opponent: {total_shots2}
        Total passes opponent: {total_passes2}
        Successful passes opponent: {successful_passes2}
        Passes into the box opponent: {passes_into_box2}
        Assists opponent: {assists2}
        Provide a 7-sentence summary of the key insights and focus on explaining the plot of successful passes into the box and assists. Use football terminology but do not complicate it.
        At the beginning explain that the red arrows showcase successful passes into the penalty box while the green dots showcase if the player assisted from that position. 
        If the team had assists highlight they had successful passes into the box that resulted in goals which helped the team get all 3 points and if they did not have assists underline that their successful passes into the box did not result in goals.
        Any assist is a positive for the team but if the team lost or drew then you can say they did not create enough chances to win.
        You can use the managers in your analysis to compliment the one who won or criticize the one who lost. You can use the stadium name as the location of the event.
        In football, every goal/assist is important to increase the winning probability of the team. You can also discuss the final result of the match."""
    
    elif plot_type == "Shots/Goals":
        df = df[df["team_name"] == team]

        total_shots = len(df[df["type_name"] == "Shot"])
        total_passes = len(df[df["type_name"] == "Pass"])
        successful_passes = len(df[(df["type_name"] == "Pass") & (~df["outcome_name"].isin(["Incomplete", "Out", "Unknown", "Pass Offside"]))])
        passes_into_box = len(df[(df["type_name"] == "Pass") & (df["end_y"] > 18) & (df["end_y"] < 62) & (df["end_x"] > 102)])
        assists = len(df[(df["type_name"] == "Pass") & (df["pass_goal_assist"] == True)])

        df2 = df[df["team_name"] == opponent]

        total_shots2 = len(df2[df2["type_name"] == "Shot"])
        total_passes2 = len(df2[df2["type_name"] == "Pass"])
        successful_passes2 = len(df2[(df2["type_name"] == "Pass") & (~df2["outcome_name"].isin(["Incomplete", "Out", "Unknown", "Pass Offside"]))])
        passes_into_box2 = len(df2[(df2["type_name"] == "Pass") & (df2["end_y"] > 18) & (df2["end_y"] < 62) & (df2["end_x"] > 102)])
        assists2 = len(df2[(df2["type_name"] == "Pass") & (df2["pass_goal_assist"] == True)])
        
        prompt = f"""You are a football analyst who needs to give his insights into the following match data information for {team} against {opponent}:
        Total shots: {total_shots}
        Total passes: {total_passes}
        Successful passes: {successful_passes}
        Passes into the box: {passes_into_box}
        Assists: {assists}
        Goals: {home_score}
        Opponents goals: {away_score}
        Home manager name: {home_manager}
        Away manager name: {away_manager}
        Stadium name: {stadium_name}
        Total shots opponent: {total_shots2}
        Total passes opponent: {total_passes2}
        Successful passes opponent: {successful_passes2}
        Passes into the box opponent: {passes_into_box2}
        Assists opponent: {assists2}
        Provide a 7-sentence summary of the key insights and focus on explaining the plot of shots (not necessarily on target) and goals. Use football terminology but do not complicate it.
        At the beginning explain that the red dots showcase shots (on target and off target, blocked or similar) while the green dots showcase goals scored from those positions. 
        If the team had goals highlight they helped their team get all 3 points especially if they won and if they did not have goals you could underline that even though they had this amount of shots they did not result in anything.
        Any goal is a positive for the team but if the team lost or drew then you can say they did not create enough chances to win.
        You can use the managers in your analysis to compliment the one who won or criticize the one who lost. You can use the stadium name as the location of the event.
        In football, every goal/assist is important to increase the winning probability of the team. You can also discuss the final result of the match."""
    
    response = model.generate_content(prompt)
    return response.text

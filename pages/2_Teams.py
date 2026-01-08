import streamlit as st
from utils.team_store import load_teams

st.title('Teams')

if "user" not in st.session_state:
    st.warning("Please login first.")
    st.stop()

# TEMP: kickoff locking stub
def is_locked(team_or_player):
    return False 

teams = load_teams()

for username, data in teams.items():
    st.subheader(username)

    roster = data["roster"]

    for slot, player in roster.items():
        if player is None:
            st.write(f"{slot}: -")
        else:
            if is_locked(player):
                st.write(f"{slot}: {player}")
            else:
                st.write(f"{slot}: 🔒 Hidden")
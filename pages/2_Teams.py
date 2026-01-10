import streamlit as st
from utils.team_store import load_teams
from utils.weekly_points import get_weekly_points


st.title('Teams')

if "unlocked_user" not in st.session_state or st.session_state.unlocked_user is None:
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
            pts = get_weekly_points(player)
            pts_display = pts if pts is not None else "—"

            if is_locked(player):
                st.write(f"{slot}: {player} ({pts_display})")
            else:
                st.write(f"{slot}: 🔒 Hidden")

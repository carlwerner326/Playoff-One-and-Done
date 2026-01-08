import streamlit as st
from utils.team_store import load_teams

# -------------------------
# Load persistent data
# -------------------------
teams = load_teams()

# -------------------------
# Session State
# -------------------------
if "unlocked_user" not in st.session_state:
    st.session_state.unlocked_user = None

# -------------------------
# Page Header
# -------------------------
st.title("Playoff Fantasy One-and-Done")

# ----- LEAGUE RULES ----
st.subheader("League Rules")
st.markdown("""
• One-and-Done playoff fantasy  
• Each player can only be used once across the playoffs  
• Lineups can be changed freely until a player's game kicks off  
• Once a game kicks off, those players are locked  
• Picks are hidden from others until each game starts  
• Highest total fantasy points after the Super Bowl wins  

• FLEX allows QB / RB / WR / TE  
• QB may be used in FLEX a maximum of **2 times**
""")

# ---- COMMISSIONER NOTE ----
st.subheader("Note")
st.markdown("""
Set your lineups early. I’m not fixing shit.  
Looking at you AJ
""")

st.divider()

# -------------------------
# Login Section
# -------------------------
user = st.selectbox("Who are you?", list(teams.keys()))

# Gate access until correct PIN is entered
if st.session_state.unlocked_user != user:
    pin = st.text_input("Enter PIN", type="password")

    if st.button("Enter"):
        if pin == teams[user]["pin"]:
            st.session_state.unlocked_user = user
            st.success("Unlocked")
        else:
            st.error("Incorrect PIN")

    st.stop()

# -------------------------
# Navigation
# -------------------------
if st.button("Go to My Team"):
    st.switch_page("pages/1_My_Team.py")

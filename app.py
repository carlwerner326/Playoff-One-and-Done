import streamlit as st
from utils.team_store import load_teams, save_teams

teams = load_teams()


# Initialize session user
if "user" not in st.session_state:
    st.session_state.user = None

if "unlocked_user" not in st.session_state:
    st.session_state.unlocked_user = None

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
""")

st.subheader("QB can be used in the FLEX spot a maximum of 2 times")

# ---- COMMISSIONER NOTE ----
st.subheader("Note")
st.markdown("""
Set your lineups early. I’m not fixing shit.  
Looking at you AJ
""")


st.divider()

user = st.selectbox("Who are you?", list(teams.keys()))

if user != st.session_state.unlocked_user:
    pin = st.text_input("Enter PIN", type="password")

    if st.button("Enter"):
        if pin == teams[user]["pin"]:
            st.session_state.unlocked_user = user
            st.success("Unlocked")
        else:
            st.error("Incorrect PIN")

    st.stop()

# ---- ADMIN TOOLS ----
if teams[st.session_state.unlocked_user]["role"] == "admin":
    st.divider()
    st.subheader("Admin Tools")

    selected_user = st.selectbox(
        "Select user",
        list(teams.keys()),
        key="admin_user_select"
    )

    new_pin = st.text_input(
        "Set new PIN",
        type="password",
        key="admin_pin_input"
    )

    if st.button("Update PIN"):
        teams[selected_user]["pin"] = new_pin
        save_teams(teams)
        st.success(f"PIN updated for {selected_user}")


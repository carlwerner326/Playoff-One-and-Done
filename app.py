import streamlit as st

USERS = {
    "Carl": "admin",
    "Jacob": "user",
    "Chris": "user",
    "Matt": "user",
    "AJ": "user",
    "Ben": "user",
    "Speedy": "user",
}

MASTER_PIN = "092391"

PINS = {
    "Carl": "092391",
    "Jacob": "1990",
    "Chris": "2323",
    "Matt": "",
    "AJ": "6969",
    "Ben": "",
    "Speedy": "",
}

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

user = st.selectbox("Who are you?", list(USERS.keys()))

if user != st.session_state.unlocked_user:
    pin = st.text_input("Enter PIN", type="password")

    if st.button("Enter"):
        if pin == PINS.get(user) or pin == MASTER_PIN:
            st.session_state.unlocked_user = user
            st.success("Unlocked")
        else:
            st.error("Incorrect PIN")

    st.stop()

    teams = load_teams()

if (
    "unlocked_user" in st.session_state
    and teams[st.session_state.unlocked_user]["role"] == "admin"
):
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



if st.button("Enter"):
    st.session_state.user = user
    st.switch_page("pages/1_My_Team.py")

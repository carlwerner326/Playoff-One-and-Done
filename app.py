import streamlit as st
from utils.team_store import load_teams
# from utils.weekly_reset import should_reset_today, perform_weekly_reset

# -------------------------
# Reset commented OUTPUT_PATH
# -------------------------
# reset_date = should_reset_today()
# if reset_date:
#    perform_weekly_reset(reset_date)

# test deploy - no functional change


# -------------------------
# Load persistent datagi
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
st.markdown("""
<h1 style="
    text-align: center;
    font-size: 3rem;
    font-weight: 800;
    margin-bottom: 1.2rem;
">
Playoff Fantasy One-and-Done
</h1>
""", unsafe_allow_html=True)

st.markdown("""
<style>
h1 {
    margin-top: 0.5rem;
}
</style>
""", unsafe_allow_html=True)



st.markdown("""
<style>
.stApp {
    background-color: #073A3D;
}

/* Push the whole page content down slightly */
.block-container {
    padding-top: 3.5rem;
}
</style>
""", unsafe_allow_html=True)



st.markdown("""
<style>
.hero-wrap {
    padding: 10px 0 30px 0;
    margin-bottom: 20px;
}

.hero-text {
    text-align: center;
    font-size: 2.4rem;
    font-weight: 900;
    color: #FFD046;
    margin-bottom: 18px;
    letter-spacing: 1px;
    text-shadow: 0 0 18px rgba(255,208,70,0.6);
}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="hero-wrap">', unsafe_allow_html=True)
st.markdown(
    '<div class="hero-text">GO FUCKING BIRDS DICKHEADS 🦅</div>',
    unsafe_allow_html=True
)
st.image("assets/hurts.png", width=900)
st.markdown('</div>', unsafe_allow_html=True)



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

if st.session_state.unlocked_user != user:
    pin = st.text_input("Enter PIN", type="password")

    if st.button("Enter"):
        user_data = teams.get(user)

        if not user_data:
            st.error("User not found.")
            st.stop()

        stored_pin = user_data.get("pin")

        if not stored_pin:
            st.error("PIN not configured for this user.")
            st.stop()

        if pin == stored_pin:
            st.session_state.unlocked_user = user
            st.success("Unlocked")
            st.rerun()
        else:
            st.error("Incorrect PIN")

    st.stop()


# -------------------------
# Navigation
# -------------------------
if st.button("Go to My Team"):
    st.switch_page("pages/1_My_Team.py")

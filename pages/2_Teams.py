import streamlit as st
from utils.team_store import load_teams
from utils.weekly_points import get_weekly_points

# --------------------------------------------------
# GLOBAL THEME / CSS (FULL PAGE)
# --------------------------------------------------
st.markdown("""
<style>

/* FULL PAGE BACKGROUND */
html, body, [class*="css"] {
    background-color: #004C54 !important;
}

.stApp {
    background-color: #004C54 !important;
}

.main {
    background-color: #004C54 !important;
}

/* Team card */
.team-card {
    background-color: #003C42;
    border-radius: 18px;
    padding: 20px;
    margin-bottom: 26px;
    box-shadow: 0 10px 26px rgba(0,0,0,0.45);
}

/* Team name */
.team-name {
    color: #FFD046;
    font-size: 1.6rem;
    font-weight: 900;
    margin-bottom: 14px;
}

/* Slot rows */
.slot-row {
    font-size: 1.1rem;
    margin: 6px 0;
    color: #FFFFFF;
}

/* Divider */
.team-divider {
    border-top: 1px solid rgba(255,255,255,0.18);
    margin: 10px 0;
}

</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# Page Header
# --------------------------------------------------
st.title("Teams")
st.markdown("---")

# --------------------------------------------------
# Auth Check
# --------------------------------------------------
if "unlocked_user" not in st.session_state or st.session_state.unlocked_user is None:
    st.warning("Please login first.")
    st.stop()

# --------------------------------------------------
# TEMP Lock Stub
# --------------------------------------------------
def is_locked(player):
    return False

# --------------------------------------------------
# Load Teams
# --------------------------------------------------
teams = load_teams()
team_items = list(teams.items())

# --------------------------------------------------
# Desktop Grid (2 columns)
# --------------------------------------------------
cols = st.columns(2)

for i, (username, data) in enumerate(team_items):
    with cols[i % 2]:

        st.markdown('<div class="team-card">', unsafe_allow_html=True)

        st.markdown(
            f'<div class="team-name">{username}</div>',
            unsafe_allow_html=True
        )

        roster = data.get("roster", {})

        for slot, player in roster.items():
            if player is None:
                st.markdown(
                    f'<div class="slot-row"><strong>{slot}:</strong> —</div>',
                    unsafe_allow_html=True
                )
            else:
                pts = get_weekly_points(player)
                pts_display = pts if pts is not None else "—"

                if is_locked(player):
                    st.markdown(
                        f'<div class="slot-row"><strong>{slot}:</strong> {player} ({pts_display})</div>',
                        unsafe_allow_html=True
                    )
                else:
                    st.markdown(
                        f'<div class="slot-row"><strong>{slot}:</strong> 🔒 Hidden</div>',
                        unsafe_allow_html=True
                    )

        st.markdown('</div>', unsafe_allow_html=True)

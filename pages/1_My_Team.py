import streamlit as st
from utils.team_store import load_teams, save_teams
import json
from pathlib import Path
from datetime import datetime, timezone

# --------------------------------------------------
# GLOBAL CSS — KELLY GREEN / GOLD THEME
# --------------------------------------------------
st.markdown("""
<style>
html, body, .stApp, .main {
    background-color: #004C54 !important;
}

h1, h2, h3 {
    color: white;
}

.stButton > button {
    width: 100%;
    text-align: left;
    font-size: 1.05rem;
    font-weight: 700;
    border-radius: 14px;
    padding: 12px 16px;
    margin-bottom: 10px;
    background-color: rgba(0,0,0,0.25);
    border: 2px solid #FFD046;
    color: white;
    box-shadow: 0 0 18px rgba(255, 208, 70, 0.25);
}

.stButton > button:hover {
    background-color: rgba(255, 208, 70, 0.15);
    border-color: #FFD046;
}

.stButton > button:disabled {
    opacity: 0.6;
    border-color: #999;
    box-shadow: none;
}

.active-slot {
    color: #FFD046;
    font-weight: 900;
}

</style>
""", unsafe_allow_html=True)

# -------------------------
# ESPN player data
# -------------------------
ESPN_PLAYERS_PATH = Path("data/espn_players.json")

def load_espn_players():
    with open(ESPN_PLAYERS_PATH) as f:
        return json.load(f)

def get_players_for_position(position):
    espn_players = load_espn_players()
    players = sorted({
        player
        for team_data in espn_players.values()
        for player in team_data.get(position, [])
    })
    return players

# -------------------------
# Session State
# -------------------------
if "active_slot" not in st.session_state:
    st.session_state.active_slot = None

# Guard: must be logged in
if "unlocked_user" not in st.session_state or st.session_state.unlocked_user is None:
    st.warning("Select your name and enter your PIN on the main page.")
    st.stop()

user = st.session_state.unlocked_user

# -------------------------
# Locking at kickoff
# -------------------------
from utils.time_lock import is_lineup_locked, get_first_kickoff_utc

locked = is_lineup_locked()
first_kickoff = get_first_kickoff_utc()
now_utc = datetime.now(timezone.utc)

# -------------------------
# Roster configuration
# -------------------------
ROSTER_SLOTS = [
    "QB","RB1","RB2","WR1","WR2","WR3","TE","FLEX","K","DST"
]

# -------------------------
# Playoff teams (DST)
# -------------------------
PLAYOFF_TEAMS_PATH = Path("data/playoff_teams.json")
with open(PLAYOFF_TEAMS_PATH) as f:
    PLAYOFF_TEAMS = json.load(f)

ALL_TEAMS = PLAYOFF_TEAMS["NFC"] + PLAYOFF_TEAMS["AFC"]

# -------------------------
# Page UI
# -------------------------
st.title("My Team")
st.subheader("My Roster")

teams = load_teams()
team = teams[user]

# -------------------------
# Roster Buttons
# -------------------------
for slot in ROSTER_SLOTS:
    player = team["roster"].get(slot)
    display = player if player else "— empty —"

    label = f"{slot}: {display}"
    if st.session_state.active_slot == slot:
        label = f"👉 {label}"

    if locked:
        st.button(
            f"{label} 🔒",
            key=f"slot_{slot}",
            disabled=True
        )
    else:
        if st.button(label, key=f"slot_{slot}"):
            st.session_state.active_slot = slot

# -------------------------
# Active Slot Indicator
# -------------------------
if st.session_state.active_slot:
    st.info(f"Active slot: {st.session_state.active_slot}")

# -------------------------
# Player Selection
# -------------------------
if st.session_state.active_slot and not locked:
    st.divider()
    st.subheader("Player Selection")

    slot = st.session_state.active_slot

    def clear_slot(slot_name):
        teams = load_teams()
        teams[user]["roster"][slot_name] = None
        save_teams(teams)
        st.session_state.active_slot = None
        st.rerun()

    def set_slot(slot_name, value):
        teams = load_teams()
        teams[user]["roster"][slot_name] = value
        save_teams(teams)
        st.session_state.active_slot = None
        st.rerun()

    # -------------------------
    # DST
    # -------------------------
    if slot == "DST":
        selected = st.selectbox(
            "Choose a Defense",
            ["— select —", "— clear —"] + ALL_TEAMS
        )

        if selected == "— clear —":
            clear_slot("DST")
        elif selected != "— select —":
            set_slot("DST", selected)

    # -------------------------
    # Standard Positions
    # -------------------------
    elif slot in ["K","QB","RB1","RB2","WR1","WR2","WR3","TE"]:
        pos = slot.replace("1","").replace("2","").replace("3","")
        players = [
            p for p in get_players_for_position(pos)
            if p not in teams[user]["used_players"]
        ]

        selected = st.selectbox(
            f"Choose {slot}",
            ["— select —", "— clear —"] + players
        )

        if selected == "— clear —":
            clear_slot(slot)
        elif selected != "— select —":
            set_slot(slot, selected)

    # -------------------------
    # FLEX
    # -------------------------
    elif slot == "FLEX":
        teams = load_teams()

        qbs = []
        if teams[user]["qb_flex_uses"] < 2:
            qbs = [
                p for p in get_players_for_position("QB")
                if p not in teams[user]["used_players"]
            ]

        rbs = [
            p for p in get_players_for_position("RB")
            if p not in teams[user]["used_players"]
        ]
        wrs = [
            p for p in get_players_for_position("WR")
            if p not in teams[user]["used_players"]
        ]
        tes = [
            p for p in get_players_for_position("TE")
            if p not in teams[user]["used_players"]
        ]

        flex_options = (
            ["— QBs —"] + qbs +
            ["— RBs —"] + rbs +
            ["— WRs —"] + wrs +
            ["— TEs —"] + tes
        )

        selected = st.selectbox(
            "Choose FLEX",
            ["— select —", "— clear —"] + flex_options
        )

        if selected == "— clear —":
            clear_slot("FLEX")
        elif selected not in [
            "— select —","— QBs —","— RBs —","— WRs —","— TEs —"
        ]:
            teams[user]["roster"]["FLEX"] = selected
            if selected in get_players_for_position("QB"):
                teams[user]["qb_flex_uses"] += 1
            save_teams(teams)
            st.session_state.active_slot = None
            st.rerun()

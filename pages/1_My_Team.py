import streamlit as st
from utils.team_store import load_teams, save_teams
import json
from pathlib import Path
from datetime import datetime, timezone

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
# Locking at kickoff (GLOBAL UI LOCK ONLY)
# -------------------------
from utils.time_lock import is_lineup_locked, get_first_kickoff_utc

locked = is_lineup_locked()
first_kickoff = get_first_kickoff_utc()
now_utc = datetime.now(timezone.utc)

# DEBUG (leave this in for now)
st.info(
    f"DEBUG LOCK STATUS\n"
    f"now_utc={now_utc}\n"
    f"first_kickoff={first_kickoff}\n"
    f"locked={locked}"
)


# -------------------------
# Roster configuration
# -------------------------
ROSTER_SLOTS = [
    "QB",
    "RB1",
    "RB2",
    "WR1",
    "WR2",
    "WR3",
    "TE",
    "FLEX",
    "K",
    "DST",
]

SLOT_ALLOWED_POSITIONS = {
    "QB": ["QB"],
    "RB1": ["RB"],
    "RB2": ["RB"],
    "WR1": ["WR"],
    "WR2": ["WR"],
    "WR3": ["WR"],
    "TE": ["TE"],
    "FLEX": ["QB", "RB", "WR", "TE"],
    "K": ["K"],
    "DST": ["DST"],
}


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

teams = load_teams()
team = teams[user]

st.subheader("My Roster")

for slot in ROSTER_SLOTS:
    player = team["roster"].get(slot)
    display = player if player else "- empty -"

    if locked:
        st.button(
            f"{slot}: {display} 🔒",
            key=f"slot_{slot}",
            disabled=True
        )
    else:
        if st.button(f"{slot}: {display}", key=f"slot_{slot}"):
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
    # K / QB / RB / WR / TE
    # -------------------------
    elif slot in ["K", "QB", "RB1", "RB2", "WR1", "WR2", "WR3", "TE"]:
        pos = slot.replace("1", "").replace("2", "").replace("3", "")
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
            "— select —",
            "— QBs —",
            "— RBs —",
            "— WRs —",
            "— TEs —",
        ]:
            teams[user]["roster"]["FLEX"] = selected
            if selected in get_players_for_position("QB"):
                teams[user]["qb_flex_uses"] += 1
            save_teams(teams)
            st.session_state.active_slot = None
            st.rerun()

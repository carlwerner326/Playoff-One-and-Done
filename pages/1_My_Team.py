import streamlit as st
from utils.team_store import load_teams, save_teams
import json
from pathlib import Path
from datetime import datetime, timezone


ESPN_PLAYERS_PATH = Path("data/espn_players.json")

def load_espn_players():
    with open(ESPN_PLAYERS_PATH) as f:
        return json.load(f)

def get_players_for_position(position):
    """
    Returns a sorted list of all players for a given position
    across all playoff teams.
    """
    espn_players = load_espn_players()

    players = sorted({
        player
        for team_data in espn_players.values()
        for player in team_data.get(position, [])
    })

    return players


# -------------------------
# Session state
# -------------------------
if "active_slot" not in st.session_state:
    st.session_state.active_slot = None

# 🔒 REQUIRED GUARD — prevents crash on refresh / deep link
if "unlocked_user" not in st.session_state or st.session_state.unlocked_user is None:
    st.warning("Select your name and enter your PIN on the main page.")
    st.stop()

user = st.session_state.unlocked_user


# -------------------------
# Locking At Kickoff
# -------------------------
from utils.time_lock import is_lineup_locked
first_kickoff = get_first_kickoff_utc()
st.info(f"DEBUG kickoff_utc={first_kickoff}, now_utc={datetime.now(timezone.utc)}")


def is_locked(_player_name=None):
    """
    Global lineup lock:
    Returns True once the first game of the weekend has kicked off.
    """
    return is_lineup_locked()


# -------------------------
# Roster
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
    "DST": ["DST"]
}


# -------------------------
# Playoff teams
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
    player = team["roster"][slot]
    display = player if player else "- empty -"

    locked = is_locked

    if locked and player not in teams[user]["used_players"]:
        teams[user]["used_players"].append(player)
        save_teams(teams)

    if locked:
        st.button(f"{slot}: {display} 🔒", key=f"slot_{slot}", disabled=True)
    else:
        if st.button(f"{slot}: {display}", key=f"slot_{slot}"):
            st.session_state.active_slot = slot



if st.session_state.active_slot:
    st.info(f"Active slot: {st.session_state.active_slot}")


# -------------------------
# Player Selection
# -------------------------
if st.session_state.active_slot:
    st.divider()
    st.subheader("Player Selection")

    if st.session_state.active_slot == "DST":
        selected_dst = st.selectbox(
            "Choose a Defense",
            ["— select —", "— clear —"] + ALL_TEAMS,
            key="dst_select"
        )

        if selected_dst == "— clear —":
            teams = load_teams()
            teams[user]["roster"]["DST"] = None
            save_teams(teams)

            st.session_state.active_slot = None
            st.rerun()
        
        elif selected_dst != "— select —":
            teams = load_teams()
            teams[user]["roster"]["DST"] = selected_dst
            save_teams(teams)

            st.session_state.active_slot = None
            st.rerun()

    elif st.session_state.active_slot == "K":
        kickers = [
            p for p in get_players_for_position("K")
            if p not in teams[user]["used_players"]
        ]

        selected_k = st.selectbox(
            "Choose a Kicker",
            ["— select —", "— clear —"] + kickers,
            key="k_select"
        )

        if selected_k == "— clear —":
            teams = load_teams()
            teams[user]["roster"]["K"] = None
            save_teams(teams)

            st.session_state.active_slot = None
            st.rerun()
        
        elif selected_k != "— select —":
            teams = load_teams()
            teams[user]["roster"]["K"] = selected_k
            save_teams(teams)

            st.session_state.active_slot = None
            st.rerun()

    elif st.session_state.active_slot == "TE":
        tes = [
            p for p in get_players_for_position("TE")
            if p not in teams[user]["used_players"]
        ]

        selected_te = st.selectbox(
            "Choose a Tight End",
            ["— select —", "— clear —"] + tes,
            key="te_select"
        )

        if selected_te == "— clear —":
            teams = load_teams()
            teams[user]["roster"]["TE"] = None
            save_teams(teams)

            st.session_state.active_slot = None
            st.rerun()
        
        elif selected_te != "— select —":
            teams = load_teams()
            teams[user]["roster"]["TE"] = selected_te
            save_teams(teams)

            st.session_state.active_slot = None
            st.rerun()

    elif st.session_state.active_slot == "QB":
        qbs = [
            p for p in get_players_for_position("QB")
            if p not in teams[user]["used_players"]
        ]

        selected_qb = st.selectbox(
            "Choose a Quarterback",
            ["— select —", "— clear —"] + qbs,
            key="qb_select"
        )

        if selected_qb == "— clear —":
            teams = load_teams()
            teams[user]["roster"]["QB"] = None
            save_teams(teams)

            st.session_state.active_slot = None
            st.rerun()
        
        elif selected_qb != "— select —":
            teams = load_teams()
            teams[user]["roster"]["QB"] = selected_qb
            save_teams(teams)

            st.session_state.active_slot = None
            st.rerun()

    elif st.session_state.active_slot == "RB1":
        rbs = [
            p for p in get_players_for_position("RB")
            if p not in teams[user]["used_players"]
        ]

        selected_rb1 = st.selectbox(
            "Choose RB",
            ["- select -", "— clear —"] + rbs,
            key="rb1_select"
        )

        if selected_rb1 == "— clear —":
            teams = load_teams()
            teams[user]["roster"]["RB1"] = None
            save_teams(teams)

            st.session_state.active_slot = None
            st.rerun()
        
        elif selected_rb1 != "- select -":
            teams = load_teams()
            teams[user]["roster"]["RB1"] = selected_rb1
            save_teams(teams)

            st.session_state.active_slot = None
            st.rerun()

    elif st.session_state.active_slot == "RB2":
        rbs = [
            p for p in get_players_for_position("RB")
            if p not in teams[user]["used_players"]
        ]

        selected_rb2 = st.selectbox(
            "Choose RB2",
            ["- select -", "— clear —"] + rbs,
            key="rb2_select"
        )

        if selected_rb2 == "— clear —":
            teams = load_teams()
            teams[user]["roster"]["RB2"] = None
            save_teams(teams)

            st.session_state.active_slot = None
            st.rerun()
        
        elif selected_rb2 != "- select -":
            teams = load_teams()
            teams[user]["roster"]["RB2"] = selected_rb2
            save_teams(teams)

            st.session_state.active_slot = None
            st.rerun()

    elif st.session_state.active_slot == "WR1":
        wrs = [
            p for p in get_players_for_position("WR")
            if p not in teams[user]["used_players"]
        ]

        selected_wr1 = st.selectbox(
            "Choose WR1",
            ["— select —", "— clear —"] + wrs,
            key="wr1_select"
        )

        if selected_wr1 == "— clear —":
            teams = load_teams()
            teams[user]["roster"]["WR1"] = None
            save_teams(teams)

            st.session_state.active_slot = None
            st.rerun()
        
        elif selected_wr1 != "— select —":
            teams = load_teams()
            teams[user]["roster"]["WR1"] = selected_wr1
            save_teams(teams)

            st.session_state.active_slot = None
            st.rerun()


    elif st.session_state.active_slot == "WR2":
        wrs = [
            p for p in get_players_for_position("WR")
            if p not in teams[user]["used_players"]
        ]

        selected_wr2 = st.selectbox(
            "Choose WR2",
            ["— select —", "— clear —"] + wrs,
            key="wr2_select"
        )

        if selected_wr2 == "— clear —":
            teams = load_teams()
            teams[user]["roster"]["WR2"] = None
            save_teams(teams)

            st.session_state.active_slot = None
            st.rerun()
        
        elif selected_wr2 != "— select —":
            teams = load_teams()
            teams[user]["roster"]["WR2"] = selected_wr2
            save_teams(teams)

            st.session_state.active_slot = None
            st.rerun()


    elif st.session_state.active_slot == "WR3":
        wrs = [
            p for p in get_players_for_position("WR")
            if p not in teams[user]["used_players"]
        ]

        selected_wr3 = st.selectbox(
            "Choose WR3",
            ["— select —", "— clear —"] + wrs,
            key="wr3_select"
        )

        if selected_wr3 == "— clear —":
            teams = load_teams()
            teams[user]["roster"]["WR3"] = None
            save_teams(teams)

            st.session_state.active_slot = None
            st.rerun()

        elif selected_wr3 != "— select —":
            teams = load_teams()
            teams[user]["roster"]["WR3"] = selected_wr3
            save_teams(teams)

            st.session_state.active_slot = None
            st.rerun()

    elif st.session_state.active_slot == "FLEX":
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

        selected_flex = st.selectbox(
            "Choose FLEX",
            ["— select —", "— clear —"] + flex_options,
            key="flex_select"
        )

        if selected_flex == "— clear —":
            teams = load_teams()
            teams[user]["roster"]["FLEX"] = None
            save_teams(teams)

            st.session_state.active_slot = None
            st.rerun()
        
        elif selected_flex not in ["— select —", "— QBs —", "— RBs —", "— WRs —", "— TEs —"]:
            teams = load_teams()
            teams[user]["roster"]["FLEX"] = selected_flex
            save_teams(teams)

            if selected_flex in get_players_for_position("QB"):
                teams[user]["qb_flex_uses"] += 1
            
            save_teams(teams)

            st.session_state.active_slot = None
            st.rerun()

    else:
        st.write("Player selection coming soon for this position.")

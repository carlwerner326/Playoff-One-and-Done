import json
import streamlit as st
from utils.team_store import load_teams

st.title("Leaderboard")

try:
    with open("data/player_points.json") as f:
        player_points = json.load(f)
except FileNotFoundError:
    player_points = {}


teams = load_teams()

rows = []

for user, data in teams.items():
    total = 0
    for player in data.get("used_players", []):
        total += player_points.get(player, 0)

    rows.append({
        "Team": user,
        "Total Points": round(total, 2)
    })

rows = sorted(rows, key=lambda x: x["Total Points"], reverse=True)

st.table(rows)

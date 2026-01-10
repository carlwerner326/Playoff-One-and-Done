import json
import streamlit as st
from utils.team_store import load_teams

# ======================================================
# PAGE BACKGROUND (Kelly Green)
# ======================================================
st.markdown(
    """
    <style>
    .stApp {
        background-color: #004C54;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ======================================================
# THEME COLORS (Gold)
# ======================================================
RANK_COLOR = "#D4AF37"      # Championship gold
POINTS_COLOR = "#D4AF37"
NAME_COLOR = "#FFFFFF"
CHAMPION_GOLD = "#FFD700"  # Brighter gold for 1st place

# ======================================================
# Page Header
# ======================================================
st.title("Leaderboard")
st.markdown("## 🏆 Playoff Fantasy One-and-Done Standings")
st.markdown("<hr style='border:1px solid rgba(255,255,255,0.25)'>", unsafe_allow_html=True)

# ======================================================
# Load player points
# ======================================================
try:
    with open("data/player_points.json") as f:
        player_points = json.load(f)
except FileNotFoundError:
    player_points = {}

# ======================================================
# Load teams and calculate totals
# ======================================================
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

# ======================================================
# Sort + Rank
# ======================================================
rows = sorted(rows, key=lambda x: x["Total Points"], reverse=True)

for i, row in enumerate(rows, start=1):
    row["Rank"] = i

# ======================================================
# Card-Style Leaderboard
# ======================================================
st.markdown("### Rankings")

for row in rows:
    cols = st.columns([1, 4, 2])

    is_champion = row["Rank"] == 1

    # Champion styling
    if is_champion:
        rank_display = "🏆 1"
        rank_color = CHAMPION_GOLD
        name_style = f"font-size:20px; color:{CHAMPION_GOLD};"
        points_style = f"color:{CHAMPION_GOLD};"
    else:
        rank_display = str(row["Rank"])
        rank_color = RANK_COLOR
        name_style = f"font-size:20px; color:{NAME_COLOR};"
        points_style = f"color:{POINTS_COLOR};"

    # Rank
    cols[0].markdown(
        f"<h3 style='color:{rank_color}; margin-bottom:0'>{rank_display}</h3>",
        unsafe_allow_html=True
    )

    # Team Name (bigger)
    cols[1].markdown(
        f"<strong style='{name_style}'>{row['Team']}</strong>",
        unsafe_allow_html=True
    )

    # Points
    cols[2].markdown(
        f"<h3 style='{points_style} margin-bottom:0'>{row['Total Points']} pts</h3>",
        unsafe_allow_html=True
    )

    st.markdown(
        "<hr style='border:1px solid rgba(255,255,255,0.25)'>",
        unsafe_allow_html=True
    )

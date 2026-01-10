import json
from pathlib import Path
from ..scoring import calculate_dk_score, DEFAULT_SETTINGS

PLAYER_STATS_PATH = Path("data/player_stats.json")

def get_weekly_points(player_name):
    if not PLAYER_STATS_PATH.exists():
        return None

    with open(PLAYER_STATS_PATH) as f:
        stats_data = json.load(f)

    player = stats_data.get(player_name)
    if not player:
        return None

    labels = player.get("raw_labels", [])
    values = player.get("raw_stats", [])
    position = player.get("position")

    stats = dict(zip(labels, values))

    try:
        return calculate_dk_score(position, stats, DEFAULT_SETTINGS)
    except Exception:
        return None

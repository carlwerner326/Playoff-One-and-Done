"""
CI-safe fantasy scoring runner.

- Reads raw ESPN stats from data/player_stats.json
- Normalizes ESPN stats into scoring.py format
- Calculates DraftKings fantasy points
- Writes data/player_points.json
- Stateless and safe for repeated runs
"""

import sys
from pathlib import Path
import json

# -------------------------
# Ensure project root is on Python path
# -------------------------
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(PROJECT_ROOT))

from scoring import calculate_dk_score, DEFAULT_SETTINGS

# -------------------------
# Paths
# -------------------------
PLAYER_STATS_PATH = Path("data/player_stats.json")
PLAYER_POINTS_PATH = Path("data/player_points.json")

# -------------------------
# ESPN → scoring.py stat key map
# -------------------------
STAT_MAP = {
    "YDS": "pass_yards",
    "TD": "pass_tds",
    "INT": "interceptions",

    "RUSH YDS": "rush_yards",
    "RUSH TD": "rush_tds",

    "REC": "receptions",
    "REC YDS": "rec_yards",
    "REC TD": "rec_tds",

    "2PT": "two_pt_conversions",
    "FUM": "fumbles_lost",

    "SACKS": "sacks",
    "INTS": "def_interceptions",
    "FR": "fumble_recoveries",
    "SAF": "safeties",
    "BLK": "blocked_kicks",
    "DEF TD": "def_tds",

    "PA": "points_allowed",
}

# -------------------------
# Helpers
# -------------------------
def normalize_stats(labels, values):
    """
    Convert ESPN label/value lists into scoring.py stat dict
    """
    stats = {}

    for label, value in zip(labels, values):
        key = STAT_MAP.get(label)
        if not key:
            continue

        try:
            stats[key] = int(value)
        except ValueError:
            continue

    return stats


def main():
    if not PLAYER_STATS_PATH.exists():
        print("No player_stats.json found — skipping scoring")
        return

    with open(PLAYER_STATS_PATH) as f:
        player_stats = json.load(f)

    if not player_stats:
        print("player_stats.json is empty — writing empty player_points.json")
        PLAYER_POINTS_PATH.parent.mkdir(parents=True, exist_ok=True)
        with open(PLAYER_POINTS_PATH, "w") as f:
            json.dump({}, f, indent=2)
        return

    player_points = {}

    for player_name, block in player_stats.items():
        try:
            position = block.get("position")
            labels = block.get("raw_labels", [])
            values = block.get("raw_stats", [])

            if not position or not labels or not values:
                continue

            stats = normalize_stats(labels, values)

            if not stats:
                continue

            points = calculate_dk_score(
                position=position,
                stats=stats,
                settings=DEFAULT_SETTINGS,
            )

            player_points[player_name] = points

        except Exception as e:
            print(f"Scoring error for {player_name}: {e}")

    PLAYER_POINTS_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(PLAYER_POINTS_PATH, "w") as f:
        json.dump(player_points, f, indent=2)

    print(f"Wrote fantasy points for {len(player_points)} players")


if __name__ == "__main__":
    main()

"""
CI-safe ESPN player stats updater.

This version is STATELESS:
- No scored_games.json
- No memory between runs
- Safe to run repeatedly (polling)

Each run rebuilds player_stats.json from scratch
based on all completed games.
"""

import json
import requests
from pathlib import Path

OUTPUT_PATH = Path("data/player_stats.json")

SCOREBOARD_URL = "https://site.api.espn.com/apis/site/v2/sports/football/nfl/scoreboard"
SUMMARY_URL = "https://site.api.espn.com/apis/site/v2/sports/football/nfl/summary?event={game_id}"


def get_completed_game_ids():
    resp = requests.get(SCOREBOARD_URL, timeout=15)
    resp.raise_for_status()
    data = resp.json()

    game_ids = []

    for event in data.get("events", []):
        if event.get("status", {}).get("type", {}).get("completed"):
            game_ids.append(event["id"])

    return game_ids


def extract_player_stats(game_id):
    resp = requests.get(SUMMARY_URL.format(game_id=game_id), timeout=15)
    resp.raise_for_status()
    data = resp.json()

    players = {}

    for team in data.get("boxscore", {}).get("players", []):
        for category in team.get("statistics", []):
            position = category.get("position")
            labels = category.get("labels", [])

            for athlete in category.get("athletes", []):
                name = athlete["athlete"]["displayName"]
                stats = athlete.get("stats", [])

                players[name] = {
                    "position": position,
                    "raw_labels": labels,
                    "raw_stats": stats,
                }

    return players


def main():
    all_players = {}

    game_ids = get_completed_game_ids()
    print(f"Found {len(game_ids)} completed games")

    for game_id in game_ids:
        print(f"Processing game {game_id}")
        game_players = extract_player_stats(game_id)
        all_players.update(game_players)

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_PATH, "w") as f:
        json.dump(all_players, f, indent=2)

    print(f"Wrote player stats for {len(all_players)} players")


if __name__ == "__main__":
    main()

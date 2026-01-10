"""
Read-only ESPN stats puller.

This script is intended to be run by GitHub Actions.
It ONLY reads ESPN data and prints results.
NO files are written.
"""

import requests

SCOREBOARD_URL = "https://site.api.espn.com/apis/site/v2/sports/football/nfl/scoreboard"

def main():
    resp = requests.get(SCOREBOARD_URL, timeout=15)
    resp.raise_for_status()
    data = resp.json()

    events = data.get("events", [])
    completed = [
        e["id"]
        for e in events
        if e.get("status", {}).get("type", {}).get("completed")
    ]

    print(f"ESPN reachable")
    print(f"Total events: {len(events)}")
    print(f"Completed games: {len(completed)}")

if __name__ == "__main__":
    main()

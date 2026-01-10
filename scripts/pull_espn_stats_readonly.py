"""
Read-only ESPN stats puller (CI probe).

This script is intended to be run by GitHub Actions.
It reads ESPN data and writes ONE safe CI-only probe file.
It does NOT touch production app data.
"""

import json
import requests
from pathlib import Path
from datetime import datetime, timezone

SCOREBOARD_URL = "https://site.api.espn.com/apis/site/v2/sports/football/nfl/scoreboard"
CI_PROBE_PATH = Path("data/_ci_probe.json")

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

    payload = {
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "total_events": len(events),
        "completed_games": len(completed),
    }

    CI_PROBE_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(CI_PROBE_PATH, "w") as f:
        json.dump(payload, f, indent=2)

    print("Wrote CI probe file:")
    print(json.dumps(payload, indent=2))

if __name__ == "__main__":
    main()

from datetime import date
import json
from pathlib import Path

WEEK_STATE_PATH = Path("data/week_state.json")

RESET_DATES = [
    date(2026, 1, 13),
    date(2026, 1, 19),
    date(2026, 1, 26),
    date(2026, 2, 9),
]

def should_reset_today():
    today = date.today()

    if not WEEK_STATE_PATH.exists():
        return False

    with open(WEEK_STATE_PATH) as f:
        state = json.load(f)

    last_reset = state.get("last_reset")
    if last_reset:
        last_reset = date.fromisoformat(last_reset)

    for reset_date in RESET_DATES:
        if today >= reset_date and (last_reset is None or last_reset < reset_date):
            return reset_date

    return False

from utils.team_store import load_teams, save_teams

def perform_weekly_reset(reset_date):
    teams = load_teams()

    for user, data in teams.items():
        # clear weekly roster
        for slot in data["roster"]:
            data["roster"][slot] = None

    save_teams(teams)

    # update reset state
    with open(WEEK_STATE_PATH, "w") as f:
        json.dump(
            {"last_reset": reset_date.isoformat()},
            f,
            indent=2
        )

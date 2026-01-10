import json
from pathlib import Path

DATA_PATH = Path("data/teams.json")

def load_teams():
    with open(DATA_PATH, "r") as f:
        return json.load(f)
    
def save_teams(data):
    with open(DATA_PATH, "w") as f:
        json.dump(data, f, indent=2)

def update_team(user, update_fn):
    teams = load_teams()
    if user not in teams:
        raise ValueError("User not found")

    update_fn(teams[user])
    save_teams(teams)
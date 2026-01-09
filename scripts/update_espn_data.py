import requests
import json

SCOREBOARD_URL = "https://site.api.espn.com/apis/site/v2/sports/football/nfl/scoreboard"
TEAMS_URL = "https://site.api.espn.com/apis/site/v2/sports/football/nfl/teams"
ROSTER_URL = "https://site.api.espn.com/apis/site/v2/sports/football/nfl/teams/{team_id}/roster"


def fetch_scoreboard():
    response = requests.get(SCOREBOARD_URL, timeout=10)
    response.raise_for_status()
    return response.json()

from datetime import datetime, timezone

def extract_kickoff_times(scoreboard_data):
    """
    Returns dict: game_id -> kickoff time (UTC ISO String)
    """
    games = {}

    for event in scoreboard_data.get("events", []):
        game_id = event.get("id")
        date_str = event.get("date")   #ISO string from ESPN

        if not game_id or not date_str:
            continue

        kickoff_utc = (
            datetime
            .fromisoformat(date_str.replace("Z", "+00:00"))
            .astimezone(timezone.utc)
            .isoformat()
        )

        games[game_id] = {
            "kickoff_utc": kickoff_utc
        }

    return games

def load_playoff_teams():
    with open("data/playoff_teams.json", "r") as f:
        data = json.load(f)

    teams = set()
    for confrence_teams in data.values():
        teams.update(confrence_teams)

    return teams

def fetch_teams():
    response = requests.get(TEAMS_URL, timeout=10)
    response.raise_for_status()
    return response.json()

def fetch_team_roster(team_id):
    url = ROSTER_URL.format(team_id=team_id)
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    return response.json()


def map_playoff_teams_to_ids(teams_data, playoff_teams):
    sports = teams_data["sports"]
    leagues = sports[0]["leagues"]
    teams = leagues[0]["teams"]

    mapping = {}

    for t in teams:
        team = t["team"]
        name = team["displayName"]
        if name in playoff_teams:
            mapping[name] = team["id"]

    return mapping

def extract_team_players(roster_data, team_name):
    allowed_positions = {"QB", "RB", "WR", "TE", "K"}

    players = {pos: [] for pos in allowed_positions}
    players["DST"] = [team_name]

    athletes = roster_data.get("athletes", [])

    for group in athletes:
        for athlete in group.get("items", []):
            pos = (
                athlete
                .get("position", {})
                .get("abbreviation")
            )

            if pos not in allowed_positions:
                continue

            name = athlete.get("displayName")
            if name:
                players[pos].append(name)

    return players






if __name__ == "__main__":
    teams_data = fetch_teams()
    playoff_teams = load_playoff_teams()
    mapping = map_playoff_teams_to_ids(teams_data, playoff_teams)

    all_rosters = {}

    for team_name, team_id in mapping.items():
        roster_data = fetch_team_roster(team_id)
        all_rosters[team_name] = extract_team_players(roster_data, team_name)
        print(f"Pulled roster for {team_name}")

    with open("data/espn_players.json", "w") as f:
        json.dump(all_rosters, f, indent=2)

    scoreboard = fetch_scoreboard()
    kickoff_times = extract_kickoff_times(scoreboard)

    with open("data/espn_games.json", "w") as f:
        json.dump(kickoff_times, f, indent=2)

    print(f"Saved espn_games.json({len(kickoff_times)} games)")

    print("\nSaved espn_players.json")


import json
from datetime import datetime, timezone
from pathlib import Path

ESPN_GAMES_PATH = Path("data/espn_games.json")


def load_espn_games():
    """
    Loads ESPN game kickoff times from disk.
    Returns dict: game_id -> { kickoff_utc }
    """
    if not ESPN_GAMES_PATH.exists():
        return {}

    with open(ESPN_GAMES_PATH, "r") as f:
        return json.load(f)


def is_game_locked(game_id):
    """
    Returns True if kickoff has passed, else False.
    Fails open (False) if game is unknown.
    """
    games = load_espn_games()

    game = games.get(str(game_id))
    if not game:
        return False

    kickoff_utc = datetime.fromisoformat(game["kickoff_utc"])
    now_utc = datetime.now(timezone.utc)

    return now_utc >= kickoff_utc


def is_game_locked_by_player(player_name, player_game_map):
    """
    Safe helper.
    Returns False if player -> game mapping does not exist.
    """
    game_id = player_game_map.get(player_name)
    if not game_id:
        return False

    return is_game_locked(game_id)

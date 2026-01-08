"""
DraftKings Scoring Engine
This module calculates fantasy points based on DK-style rules
"""

# -------------------------
# DEFAULT SCORING SETTINGS
# -------------------------

DEFAULT_SETTINGS = {
    # Passing
    "pass_yds_per_point": 25,
    "pass_tds_points": 4,
    "int_penalty": 1,
    "bonus_300_pass": True,
    "bonus_300_pass_points": 3,

    # RUSHING / RECEIVINGalright 
    "rush_yds_per_point": 10,
    "rec_yds_per_point": 10,
    "rush_tds_points": 6,
    "rec_tds_points": 6,

    # RECEPTIONS
    "ppr": 1,

    # MISC
    "fumble_penalty": 1,
    "two_pt_points": 2,

    # Bonuses
    "bonus_100_rush": True,
    "bonus_100_rec": True,
    "bonus_100_points": 3,

    # Kicking 
    "xp_points": 1,
    "xp_miss_penalty": 1,

    "fg_0_39_points": 3,
    "fg_40_49_points": 4,
    "fg_50_plus_points": 5,

    "fg_miss_penalty": 1,

    # DEFENSE / SPECIAL TEAMS
    "sack_points": 1,
    "int_points": 2,
    "fumble_recovery_points": 2,
    "safety_points": 2,
    "blocked_kick_points": 2,
    "def_td_points": 6,

}

def calculate_dk_score(position, stats, settings):
    """
    Docstring for calculate_dk_score
    
    :param position: str (QB, RB, WR, TE, K, DST)
    :param stats: dict of raw stat values
    :param settings: dict of rule toggles and penalties
    """

    points = 0.0

    # -----------------
    # PASSING
    # -----------------
    pass_yards = stats.get("pass_yards", 0)
    pass_tds = stats.get("pass_tds", 0)
    interceptions = stats.get("interceptions", 0)

    if pass_yards > 0 or pass_tds > 0 or interceptions > 0:
        points += pass_yards / settings["pass_yds_per_point"]
        points += pass_tds * settings["pass_tds_points"]
        points -= interceptions * settings["int_penalty"]

        if settings["bonus_300_pass"] and pass_yards >= 300:
            points += settings["bonus_300_pass_points"]

    
    # -----------------
    # RUSHING
    # -----------------
    rush_yards = stats.get("rush_yards", 0)
    rush_tds = stats.get("rush_tds", 0)

    if rush_yards > 0 or rush_tds > 0:
        points += rush_yards / settings["rush_yds_per_point"]
        points += rush_tds * settings["rush_tds_points"]


    # ------------------
    # RECEIVING
    # ------------------
    rec_yards = stats.get("rec_yards", 0)
    rec_tds = stats.get("rec_tds", 0)
    receptions = stats.get("receptions", 0)

    if rec_yards > 0 or rec_tds > 0 or receptions > 0:
        points += rec_yards / settings["rec_yds_per_point"]
        points += rec_tds * settings["rec_tds_points"]
        points += receptions * settings["ppr"]


    # ------------------
    # YARDAGE BONUSES
    # ------------------
    if settings.get("bonus_100_rush") and rush_yards >= 100:
        points += settings.get("bonus_100_points", 3)
    
    if settings.get("bonus_100_rec") and rec_yards >= 100:
        points += settings.get("bonus_100_points", 3)

    
    # ------------------
    # MISC
    # ------------------
    two_pt = stats.get("two_pt_conversions", 0)
    fumbles = stats.get("fumbles_lost", 0)

    points += two_pt * settings["two_pt_points"]
    points -= fumbles * settings["fumble_penalty"]


    # ------------------
    # KICKING
    # ------------------
    xp_made = stats.get("xp_made", 0)
    xp_missed = stats.get("xp_missed", 0)

    fg_0_39 = stats.get("fg_made_0_39", 0)
    fg_40_49 = stats.get("fg_made_40_49", 0)
    fG_50_plus = stats.get("fg_made_50_plus", 0)
    fg_missed = stats.get("fg_missed", 0)

    points += xp_made * settings["xp_points"]
    points -= xp_missed * settings["xp_miss_penalty"]

    points += fg_0_39 * settings["fg_0_39_points"]
    points += fg_40_49 * settings["fg_40_49_points"]
    points += fG_50_plus * settings["fg_50_plus_points"]
    points -= fg_missed * settings["fg_miss_penalty"]


    # ------------------
    # DEFENSE / SPECIAL TEAMS
    # ------------------
    sacks = stats.get("sacks", 0)
    ints= stats.get("def_interceptions", 0)
    fumble_recoveries = stats.get("fumble_recoveries", 0)
    safeties = stats.get("safeties", 0)
    blocked_kicks = stats.get("blocked_kicks", 0)
    def_tds = stats.get("def_tds", 0)

    points += sacks * settings["sack_points"]
    points += ints * settings["int_points"]
    points += fumble_recoveries * settings["fumble_recovery_points"]
    points += safeties * settings["safety_points"]
    points += blocked_kicks * settings["blocked_kick_points"]
    points += def_tds * settings["def_td_points"]


    return round(points, 2)


if __name__ == "__main__":
    test_stats = {
        # Kicker
        "xp_made": 3,
        "xp_missed": 1,
        "fg_made_0_39": 1,
        "fg_made_40_49": 1,
        "fg_made_50_plus": 1,
        "fg_missed": 1,

        # DST
        "sacks": 4,
        "def_interceptions": 1,
        "fumble_recoveries": 1,
        "safeties": 0,
        "blocked_kicks": 1,
        "def_tds": 1,
    }

    score = calculate_dk_score(
        position="DST",
        stats=test_stats,
        settings=DEFAULT_SETTINGS
    )

    print("K + DST Score:", score)



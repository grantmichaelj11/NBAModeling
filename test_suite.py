"""Data-integrity checks for the NBA database, plus unit tests for the helpers.

The integrity tests need a reachable MySQL server and are skipped when there
isn't one. The helper tests use small in-memory data and always run.
Nothing here touches the database at import time, so collection never fails.
"""
import numpy as np
import pytest
from mysql.connector.errors import InterfaceError

import db_connection as connect

DATABASE = "NBA"


# --------------------------------------------------------------------------
# Database access
# --------------------------------------------------------------------------

def _fetch_all(query, database=DATABASE):
    with connect.connect_to_database(database) as conn:
        cursor = conn.cursor()
        try:
            cursor.execute(query)
            return cursor.fetchall()
        finally:
            cursor.close()


def acquire_all_boxscores(database=DATABASE):
    return _fetch_all("SELECT * FROM boxscores", database)


def acquire_all_games_team(database=DATABASE):
    return _fetch_all("SELECT boxscore FROM team_stats", database)


# --------------------------------------------------------------------------
# Pure helpers (no database)
# --------------------------------------------------------------------------

def create_boxscore_array(rows):
    """First column of each row as a numpy array (works for int or str ids)."""
    return np.array([row[0] for row in rows])


def team_stats_without_two_rows(team_boxscores):
    """Boxscore ids that don't appear exactly twice (one row per team)."""
    ids, counts = np.unique(team_boxscores, return_counts=True)
    return ids[counts != 2]


def ensure_duplicates_for_all_team_stats(team_boxscores):
    """True if every game has team stats for both teams."""
    return team_stats_without_two_rows(team_boxscores).size == 0


def find_boxscores_not_in_stats(boxscores, stats):
    """Boxscore ids with no matching team-stat rows."""
    return np.setdiff1d(boxscores, np.unique(stats))


# --------------------------------------------------------------------------
# Fixtures: load once per session, skip cleanly if MySQL is unreachable
# --------------------------------------------------------------------------

def _load_ids(loader):
    try:
        return create_boxscore_array(loader())
    except InterfaceError as e:
        pytest.skip(f"MySQL not reachable: {e}")


@pytest.fixture(scope="session")
def boxscores():
    return _load_ids(acquire_all_boxscores)


@pytest.fixture(scope="session")
def team_stats():
    return _load_ids(acquire_all_games_team)


# --------------------------------------------------------------------------
# Integrity tests (need the real database)
# --------------------------------------------------------------------------

def test_every_game_has_two_team_stat_rows(team_stats):
    bad = team_stats_without_two_rows(team_stats)
    assert bad.size == 0, (
        f"{bad.size} games don't have exactly two team-stat rows, e.g. {bad[:20].tolist()}"
    )


def test_every_boxscore_has_team_stats(boxscores, team_stats):
    missing = find_boxscores_not_in_stats(boxscores, team_stats)
    assert missing.size == 0, (
        f"{missing.size} boxscores have no team stats, e.g. {missing[:20].tolist()}"
    )


# --------------------------------------------------------------------------
# Unit tests for the helpers (always run)
# --------------------------------------------------------------------------

def test_create_boxscore_array_takes_first_column():
    rows = [(101, "a", 3), (102, "b", 4)]
    assert create_boxscore_array(rows).tolist() == [101, 102]


def test_create_boxscore_array_handles_string_ids():
    rows = [("202412010BOS",), ("202412010LAL",)]
    assert create_boxscore_array(rows).tolist() == ["202412010BOS", "202412010LAL"]


def test_create_boxscore_array_empty():
    assert create_boxscore_array([]).size == 0


def test_duplicate_check_passes_when_every_game_has_both_teams():
    assert ensure_duplicates_for_all_team_stats(np.array([1, 1, 2, 2]))


def test_duplicate_check_flags_missing_and_extra_rows():
    ids = np.array([1, 1, 2, 3, 3, 3])
    assert not ensure_duplicates_for_all_team_stats(ids)
    assert team_stats_without_two_rows(ids).tolist() == [2, 3]


def test_find_boxscores_not_in_stats():
    boxscores = np.array([1, 2, 3])
    stats = np.array([1, 1, 3, 3])
    assert find_boxscores_not_in_stats(boxscores, stats).tolist() == [2]

import pytest
from logic_utils import check_guess, update_score, parse_guess, get_range_for_difficulty


# --- check_guess tests ---

def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win
    result = check_guess(50, 50)
    assert result == "Win"

def test_guess_too_high():
    # If secret is 50 and guess is 60, hint should be "Too High"
    result = check_guess(60, 50)
    assert result == "Too High"

def test_guess_too_low():
    # If secret is 50 and guess is 40, hint should be "Too Low"
    result = check_guess(40, 50)
    assert result == "Too Low"

# FIX: Regression test for Bug 1 — hints were backwards.
def test_too_high_means_player_overshot():
    """Guess above the secret must return Too High (player should go lower)."""
    assert check_guess(75, 50) == "Too High"
    assert check_guess(99, 1) == "Too High"

def test_too_low_means_player_undershot():
    """Guess below the secret must return Too Low (player should go higher)."""
    assert check_guess(25, 50) == "Too Low"
    assert check_guess(1, 99) == "Too Low"

# FIX: Regression test for Bug 4 — integer comparison, not lexicographic string comparison.
def test_check_guess_uses_integer_comparison():
    """'9' > '10' is True for strings but 9 < 10 numerically — must use integers."""
    assert check_guess(9, 10) == "Too Low"
    assert check_guess(10, 9) == "Too High"
    assert check_guess(2, 19) == "Too Low"


# --- update_score tests ---

# FIX: Regression test for Bug 5 — wrong guesses must always cost points.
def test_too_high_always_subtracts_points():
    """Too High should subtract 5 points on every attempt, including even ones."""
    assert update_score(100, "Too High", 2) == 95   # even attempt — was +5 before fix
    assert update_score(100, "Too High", 3) == 95   # odd attempt
    assert update_score(100, "Too High", 4) == 95   # even attempt

def test_too_low_subtracts_points():
    assert update_score(100, "Too Low", 1) == 95
    assert update_score(100, "Too Low", 2) == 95

def test_win_adds_points():
    # attempt_number=1: points = 100 - 10*(1+1) = 80
    assert update_score(0, "Win", 1) == 80

def test_win_minimum_points():
    # High attempt numbers should award at least 10 points
    assert update_score(0, "Win", 20) == 10


# --- get_range_for_difficulty tests ---

# FIX: Regression test for Bug 2 — Hard must be harder than Normal.
def test_hard_range_wider_than_normal():
    _, normal_high = get_range_for_difficulty("Normal")
    _, hard_high = get_range_for_difficulty("Hard")
    assert hard_high > normal_high, "Hard difficulty should have a wider range than Normal"

def test_easy_range():
    low, high = get_range_for_difficulty("Easy")
    assert low == 1
    assert high == 20

def test_normal_range():
    low, high = get_range_for_difficulty("Normal")
    assert low == 1
    assert high == 100


# --- parse_guess tests ---

def test_parse_valid_integer():
    ok, value, err = parse_guess("42")
    assert ok is True
    assert value == 42
    assert err is None

def test_parse_empty_string():
    ok, value, err = parse_guess("")
    assert ok is False
    assert value is None

def test_parse_none():
    ok, value, err = parse_guess(None)
    assert ok is False
    assert value is None

def test_parse_non_number():
    ok, value, err = parse_guess("abc")
    assert ok is False
    assert "not a number" in err.lower()

def test_parse_float_rounds_to_int():
    ok, value, err = parse_guess("3.7")
    assert ok is True
    assert value == 3

# FIX: All game logic refactored from app.py into logic_utils.py using Copilot Agent mode.


def get_range_for_difficulty(difficulty: str):
    """Return (low, high) inclusive range for a given difficulty."""
    if difficulty == "Easy":
        return 1, 20
    if difficulty == "Normal":
        return 1, 100
    # FIX (Bug 2): Hard was returning (1, 50) — narrower than Normal, making it easier.
    #              Now returns (1, 500) so Hard is genuinely harder than Normal.
    if difficulty == "Hard":
        return 1, 500
    return 1, 100


def parse_guess(raw: str):
    """
    Parse user input into an int guess.

    Returns: (ok: bool, guess_int: int | None, error_message: str | None)
    """
    if raw is None or raw == "":
        return False, None, "Enter a guess."
    try:
        if "." in raw:
            value = int(float(raw))
        else:
            value = int(raw)
    except Exception:
        return False, None, "That is not a number."
    return True, value, None


def check_guess(guess: int, secret: int) -> str:
    """
    Compare guess to secret and return outcome string.

    Returns: "Win", "Too High", or "Too Low"
    """
    # FIX (Bug 1): Hints were completely backwards. guess > secret means the player
    #              guessed too high and should go lower — not higher.
    if guess == secret:
        return "Win"
    if guess > secret:
        return "Too High"
    return "Too Low"


def update_score(current_score: int, outcome: str, attempt_number: int) -> int:
    """Update score based on outcome and attempt number."""
    if outcome == "Win":
        points = 100 - 10 * (attempt_number + 1)
        if points < 10:
            points = 10
        return current_score + points
    # FIX (Bug 5): Removed the parity check that added +5 points on even attempts for
    #              a wrong "Too High" guess. Wrong guesses always subtract points now.
    if outcome == "Too High":
        return current_score - 5
    if outcome == "Too Low":
        return current_score - 5
    return current_score

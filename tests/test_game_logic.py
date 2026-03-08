# FIX: Added conftest.py at the project root so pytest can resolve from logic_utils import ... from the tests subdirectory
from logic_utils import check_guess

# FIX (for 3 starter tests): originally comparing full tuple against a plain string which would never match, now unpacks
def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win
    outcome, message = check_guess(50, 50)
    assert outcome == "Win"

def test_guess_too_high():
    # If secret is 50 and guess is 60, hint should be "Too High"
    outcome, message = check_guess(60, 50)
    assert outcome == "Too High"

def test_guess_too_low():
    # If secret is 50 and guess is 40, hint should be "Too Low"
    outcome, message = check_guess(40, 50)
    assert outcome == "Too Low"


# Tests targeting the reversed-hints bug:
# Previously, guessing too high returned "Go HIGHER!" and too low returned "Go LOWER!" — the opposite of correct.

def test_too_high_message_says_go_lower():
    # Guess is above the secret, so the player needs to go lower
    outcome, message = check_guess(80, 50)
    assert outcome == "Too High"
    assert "LOWER" in message, f"Expected 'LOWER' in hint for too-high guess, got: '{message}'"
    assert "HIGHER" not in message, f"Hint should not say 'HIGHER' for a too-high guess, got: '{message}'"

def test_too_low_message_says_go_higher():
    # Guess is below the secret, so the player needs to go higher
    outcome, message = check_guess(20, 50)
    assert outcome == "Too Low"
    assert "HIGHER" in message, f"Expected 'HIGHER' in hint for too-low guess, got: '{message}'"
    assert "LOWER" not in message, f"Hint should not say 'LOWER' for a too-low guess, got: '{message}'"


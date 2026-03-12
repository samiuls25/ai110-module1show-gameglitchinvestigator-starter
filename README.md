# 🎮 Game Glitch Investigator: The Impossible Guesser

## 🚨 The Situation

You asked an AI to build a simple "Number Guessing Game" using Streamlit.
It wrote the code, ran away, and now the game is unplayable.

- You can't win.
- The hints lie to you.
- The secret number seems to have commitment issues.

## 🛠️ Setup

1. Install dependencies: `pip install -r requirements.txt`
2. Run the broken app: `python -m streamlit run app.py`

## 🕵️‍♂️ Your Mission

1. **Play the game.** Open the "Developer Debug Info" tab in the app to see the secret number. Try to win.
2. **Find the State Bug.** Why does the secret number change every time you click "Submit"? Ask ChatGPT: *"How do I keep a variable from resetting in Streamlit when I click a button?"*
3. **Fix the Logic.** The hints ("Higher/Lower") are wrong. Fix them.
4. **Refactor & Test.** - Move the logic into `logic_utils.py`.
   - Run `pytest` in your terminal.
   - Keep fixing until all tests pass!

## 📝 Document Your Experience

- [ ] Describe the game's purpose.
- [ ] Detail which bugs you found.
- [ ] Explain what fixes you applied.


---

## 📝 Game Purpose

A number guessing game built with Streamlit. The app picks a secret number within a range determined by the chosen difficulty (Easy: 1–20, Normal: 1–100, Hard: 1–50). The player has a limited number of attempts to guess the secret number, receiving Higher/Lower hints after each guess. A score is tracked throughout the game and decreases with wrong guesses.

---

## 🐛 Bugs Found

### Bug 1 — `attempts` initialized to `1` instead of `0`
`st.session_state.attempts` started at `1`, which caused an off-by-one error throughout the game. Score calculations and attempt counting were all shifted by one from the very first guess.

### Bug 2 — Secret forced to convert to a string on even attempts
On every even attempt, the local `secret` variable was converted to a string (`str(st.session_state.secret)`). When `check_guess` received mismatched types (`int` vs `str`), Python fell into the `except TypeError` branch which performed **alphabetical string comparison** instead of numeric comparison. This made the game behave as if the secret number was changing on every other guess.

### Bug 3 — Submit button appeared to do nothing on the first click
The debug expander was rendered **before** the `if submit:` block. Because Streamlit renders top-to-bottom on every run, the expander always captured session state values from *before* the submit logic ran. This made it look like nothing happened on the first click - hints appeared (rendered inside the submit block) but the debug info stayed stale until the next run.

### Bug 4 — Hints were reversed
In `check_guess`, `guess > secret` (guess is too high) returned `"📈 Go HIGHER!"` and `guess < secret` (guess is too low) returned `"📉 Go LOWER!"` — the exact opposite of correct.

### Bug 5 — Hints stopped showing after fixing Bug 3
After adding `st.rerun()` at the end of the submit block to fix the debug panel, `st.warning(message)` was being called and then immediately discarded before it could render, because `st.rerun()` restarts the script before Streamlit flushes the UI.

---

## 🔧 Fixes Applied

| Bug | Fix |
|-----|-----|
| `attempts` starts at `1` | Changed initial value to `0` |
| Secret type-switching | Removed the even/odd forced conversion; always use `st.session_state.secret` as an `int` |
| Debug panel shows stale state | Added `st.rerun()` after the submit block and moved debug expander above the input with `expanded=True` to persist its open state |
| Reversed hints | Swapped the messages: `guess > secret` → `"Go LOWER!"`, `guess < secret` → `"Go HIGHER!"` |
| Hints not showing after rerun | Saved the hint to `st.session_state.hint` inside the submit block and rendered it from session state on the next run |

---

## ♻️ Refactor

All core game logic was moved out of `app.py` and into `logic_utils.py`:

- `get_range_for_difficulty`
- `parse_guess`
- `check_guess`
- `update_score`

`app.py` now imports from `logic_utils` and contains only Streamlit UI code.

---

## 🧪 Tests

Run tests with:

```bash
pytest tests/test_game_logic.py -v
```

The test covers:

| Test | What it checks |
|------|----------------|
| `test_winning_guess` | Correct guess returns `"Win"` outcome |
| `test_guess_too_high` | Guess above secret returns `"Too High"` outcome |
| `test_guess_too_low` | Guess below secret returns `"Too Low"` outcome |
| `test_too_high_message_says_go_lower` | Regression — too-high hint contains `"LOWER"`, not `"HIGHER"` |
| `test_too_low_message_says_go_higher` | Regression — too-low hint contains `"HIGHER"`, not `"LOWER"` |

> **Note:** A root-level `conftest.py` was added so pytest can resolve `logic_utils` from the `tests/` subdirectory.

---

## 📸 Demo

- [ ] [Insert a screenshot of your fixed, winning game here]

## 🚀 Stretch Features

- [ ] [If you choose to complete Challenge 4, insert a screenshot of your Enhanced Game UI here]

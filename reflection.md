# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

When the game first launched it appeared to work, but playing it revealed several clear bugs immediately.

**Bug 1 – Hints are completely backwards (`check_guess` in app.py)**

- **Expected:** When my guess is too high, the hint should say "Go LOWER!" to tell me to guess a smaller number. When my guess is too low, the hint should say "Go HIGHER!".
- **What actually happened:** The hint said "📈 Go HIGHER!" when my guess was above the secret number, and "📉 Go LOWER!" when it was below it — the exact opposite of correct. Every hint actively misled me in the wrong direction.
- **Root cause:** In `check_guess()`, the condition `if guess > secret` returns the message `"📈 Go HIGHER!"` when it should return `"📉 Go LOWER!"`, and vice versa.

**Bug 2 – "Hard" difficulty is easier than "Normal" (`get_range_for_difficulty` in app.py)**

- **Expected:** Increasing difficulty should make the game harder. "Hard" should have a larger number range than "Normal" to make guessing harder.
- **What actually happened:** Easy gives a range of 1–20, Normal gives 1–100, but Hard gives only 1–50. Hard is actually easier than Normal because the range is smaller, making the secret number easier to guess.
- **Root cause:** The `if difficulty == "Hard"` branch returns `(1, 50)` instead of a larger range like `(1, 500)`.

**Bug 3 – New game doesn't reset game status, so new rounds are unplayable after a win or loss**

- **Expected:** Clicking "New Game 🔁" should fully reset the game so I can play again from scratch.
- **What actually happened:** After winning or losing, clicking "New Game" reset the secret number and attempt count but left `st.session_state.status` as `"won"` or `"lost"`. The app immediately hit the status check and displayed "You already won. Start a new game to play again." — blocking all input and making the fresh game unplayable.
- **Root cause:** The `new_game` handler in app.py never resets `st.session_state.status` back to `"playing"`.

**Bug 4 – Even-numbered attempts switch the secret to a string, causing wrong outcomes**

- **Expected:** Every guess should be compared numerically to the secret number.
- **What actually happened:** On every even attempt (2nd, 4th, 6th…), the code converts the integer secret to a string before calling `check_guess`. This triggers the string-comparison fallback path inside `check_guess`, which compares strings lexicographically (e.g., `"9" > "10"` is `True` in Python). This means a guess of 9 is reported as "Too High" when the secret is 10 — numerically wrong.
- **Root cause:** `if st.session_state.attempts % 2 == 0: secret = str(st.session_state.secret)` in app.py intentionally (or accidentally) switches the type every other turn.

**Bug 5 – Guessing too high on even attempts rewards points instead of penalising them**

- **Expected:** Any incorrect guess should reduce my score.
- **What actually happened:** In `update_score`, when `outcome == "Too High"` and `attempt_number % 2 == 0`, the function returns `current_score + 5` — adding points for a wrong answer. On odd attempts the same wrong guess correctly subtracts 5 points.
- **Root cause:** The parity check `if attempt_number % 2 == 0` inside the `"Too High"` branch flips the sign of the score change depending on the attempt number.

**Bug 6 – Info bar always says "1 and 100" regardless of difficulty**

- **Expected:** The instruction text should tell me the actual range for the selected difficulty (e.g., "1 and 20" for Easy).
- **What actually happened:** The `st.info(...)` call in app.py has the range hardcoded as `"Guess a number between 1 and 100"` and never uses the `low` / `high` variables, so Easy and Hard both display the wrong range.

---

## 2. How did you use AI as a teammate?

I used GitHub Copilot (in VS Code) as my primary AI tool throughout this project. I used the `#file:app.py` and `#file:logic_utils.py` context variables to give Copilot a full view of the codebase before asking questions, which made its answers much more specific than generic explanations.

**Correct suggestion:** I asked Copilot to explain what happened on even-numbered attempts by highlighting the block `if st.session_state.attempts % 2 == 0: secret = str(st.session_state.secret)` and using Inline Chat to ask "Explain this logic step-by-step." Copilot correctly identified that converting the secret to a string would cause Python's `TypeError` when comparing `int > str`, which would fall into the `except` block and use lexicographic string comparison — producing wrong results for any two-digit secret. I verified this by mentally tracing the code path: `check_guess(9, "10")` raises `TypeError`, catches it, then evaluates `"9" > "10"` which is `True` in Python, so it returns "Too High" — confirmed wrong.

**Incorrect/misleading suggestion:** When I first asked Copilot "why is the score sometimes going up when I guess wrong?", it initially suggested the issue might be a display/rendering bug where Streamlit was showing a cached state value. This was misleading — the real issue was a logic bug in `update_score` where `attempt_number % 2 == 0` explicitly adds 5 points for a "Too High" guess. I verified the actual cause by reading the `update_score` function directly and tracing through with attempt number 2: the condition `if attempt_number % 2 == 0` evaluated to `True`, returning `current_score + 5` instead of `current_score - 5`.

---

## 3. Debugging and testing your fixes

I decided a bug was really fixed when three things were true: (1) I could reproduce the original failure before touching the code, (2) after the fix the same input produced the correct result, and (3) an automated pytest test I wrote specifically for that bug passed with a green checkmark. "It seems to work now" wasn't enough — I needed a repeatable, objective signal.

**Tests I ran:** I ran `python -m pytest tests/test_game_logic.py -v` and all 18 tests passed in 0.07 s. The suite covers every fixed function:

- `test_too_high_means_player_overshot` and `test_too_low_means_player_undershot` — regression tests for Bug 1. Before the fix, `check_guess(75, 50)` returned `"Too Low"` instead of `"Too High"`. After swapping the logic in `logic_utils.py`, both tests pass.
- `test_check_guess_uses_integer_comparison` — regression test for Bug 4. The key assertion is `check_guess(9, 10) == "Too Low"` (9 is less than 10 numerically, but `"9" > "10"` is `True` in Python string comparison). Before the refactor removed the string conversion, this would have returned `"Too High"`.
- `test_too_high_always_subtracts_points` — regression test for Bug 5. It checks `update_score(100, "Too High", 2) == 95` specifically on an even attempt number, where the old code returned `current_score + 5` instead of `-5`.
- `test_hard_range_wider_than_normal` — regression test for Bug 2. It asserts `hard_high > normal_high`, catching any future regression where Hard is accidentally made narrower than Normal.

**AI help with tests:** I asked Copilot to suggest edge-case inputs for `test_check_guess_uses_integer_comparison`. It recommended adding `check_guess(2, 19) == "Too Low"` since `"2" > "19"` is `True` in Python string comparison (the string `"2"` sorts after `"1"`), making it a clean, concrete example that exposes the lexicographic failure mode. That suggestion went directly into the test.

---

## 4. What did you learn about Streamlit and state?

Streamlit works differently from a traditional program: every time a user clicks a button or changes any input, Streamlit reruns the entire Python script from the top. This means normal Python variables are reset to their initial values on every rerun — so if you just wrote `score = 0` at the top of the file, clicking a button would wipe out any score you had accumulated.

To keep data alive across reruns, Streamlit provides `st.session_state`, which is a dictionary-like object that persists for the lifetime of a browser session. Think of it like a notepad that survives even when the script is rerun from line 1. When I click "Submit Guess", the script reruns, but `st.session_state.score`, `st.session_state.attempts`, and `st.session_state.secret` all retain their previous values because they live in session state instead of local variables. Without this, every button click would restart the game from scratch invisibly — which is exactly why Bug 3 (forgetting to reset `st.session_state.status` in the new game handler) was so disruptive.

---

## 5. Looking ahead: your developer habits

**Habit to reuse:** Reading every function with fresh eyes before trusting it — especially in AI-generated code. My habit going forward is to trace at least one concrete example through any function that involves conditionals or comparisons before accepting it as correct. In this project, mentally running `check_guess(75, 50)` immediately revealed the backwards hint. That 30-second trace saved significant debugging time later.

**What I'd do differently:** Next time I work with AI on a coding task, I would ask the AI to explain *why* it wrote each branching condition rather than just accepting the generated code. In this project, the `if attempt_number % 2 == 0: secret = str(...)` line looks intentional and syntactically valid — AI didn't flag it as suspicious. Asking "what is the purpose of this line and what happens if I remove it?" would have surfaced both Bug 4 and Bug 5 immediately.

**How this changed my thinking:** This project made me treat AI-generated code the same way I would treat code written by a new teammate who is fast but sometimes overconfident — useful output that still requires review, not finished work I can ship blindly. AI can write plausible-looking code that contains subtle, compounding logic errors (like the type-switch combined with the score parity flip) that are intentionally hard to spot in isolation but break the game in practice.

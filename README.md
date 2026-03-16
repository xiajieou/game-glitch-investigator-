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

- The game's purpose is to practice debugging an AI-generated Streamlit app by observing broken behavior, tracing logic, and validating fixes with tests.
- Bugs found included backwards higher/lower hints, a misleading Hard difficulty range, new-game state not resetting correctly, even-attempt type switching (`int` to `str`) causing wrong comparisons, and score inconsistencies on incorrect guesses.
- Fixes applied included refactoring core logic into `logic_utils.py`, repairing `check_guess`, `update_score`, and difficulty range logic, resetting status on new game, removing string-conversion comparison bugs, and adding regression-focused pytest coverage.

## 📸 Demo

![Winning game screenshot](assets/winning-game.png)

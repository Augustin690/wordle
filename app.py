from flask import Flask, render_template, request, jsonify
from wordle import guess_wordle
app = Flask(__name__)

word_size = 5
attempt = 0
max_attempts = 5

# In-memory game state
game_state = {"attempts": [], "status": "ongoing"}


@app.route("/")
def index():
    # Initialize game state if not done yet
    if "letter_feedback" not in game_state:
        game_state["letter_feedback"] = {}

    return render_template("index.html", game_state=game_state, word_size=word_size, max_attempts=max_attempts)

@app.route("/guess", methods=["POST"])
def guess():
    global attempt

    if attempt >= max_attempts:
        return jsonify({"error": "Game Over!"}), 400

    guess_word = request.form["guess"].lower()
    if len(guess_word) != word_size:
        return jsonify({"error": f"Word must be {word_size} letters."}), 400

    feedback_result = guess_wordle("/random", guess_word)

    # Update letter feedback for the alphabet grid
    letter_feedback = game_state.get("letter_feedback", {})

    for i, letter in enumerate(guess_word):
        feedback = feedback_result[i].get("result")
        if feedback == "correct":
            letter_feedback[letter] = "correct"
        elif feedback == "present":
            letter_feedback[letter] = "present"
        else:
            letter_feedback[letter] = "absent"

    # Update the game state with the letter feedback
    game_state["letter_feedback"] = letter_feedback

    # Update game state with the guess and feedback
    game_state["attempts"].append({"guess": guess_word, "feedback": feedback_result})
    attempt += 1

    if all(r.get("result") == "correct" for r in feedback_result):
        game_state["status"] = "win"
        return jsonify({"message": "Congratulations! You guessed the word!"}), 200  # Success response

    return jsonify({"feedback": feedback_result}), 200  # Regular feedback response



if __name__ == "__main__":
    app.run(debug=True)

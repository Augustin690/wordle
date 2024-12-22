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

    # Update game state
    game_state["attempts"].append({"guess": guess_word, "feedback": feedback_result})
    attempt += 1

    if  all(r["result"] == "correct" for r in feedback_result):
        game_state["status"] = "win"
        return jsonify({"message": "Congratulations! You guessed the word."})

    if attempt >= max_attempts:
        game_state["status"] = "lose"
        return jsonify({"message": "Game Over! You've used all attempts."})

    return jsonify({"feedback": feedback_result})


if __name__ == "__main__":
    app.run(debug=True)

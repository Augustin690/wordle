"""Your task is to write a program that automatically guesses random words"""

import requests
import random
import tkinter as tk
from tkinter import messagebox

api_url = "https://wordle.votee.dev:8000/"

# guess types : "/random", "/daily", "/word/"
def guess_wordle(guess_type: str, guess: str, size: int=5, seed: int=0, target: str = "word"):
    """ Function to guess a word """

    if guess_type == "/random":
        response = requests.get(api_url + guess_type, {"guess": guess, "size": size, "seed": seed})
        print(response.json())
        return response.json()

    if guess_type == "/word/":

        # need to check if guess and target have the same length
        try:
            assert(len(guess) == len(target))

        except AssertionError:
            print("Guess type and target must be same length")
            return 0

        response = requests.get(api_url + guess_type + target, {"guess": guess, "size": len(target)})
        print(response.json())
        return response.json()

    response = requests.get(api_url + guess_type, {"guess": guess, "size": size})
    print(response.json())
    return response.json()

# Function to interact with the Wordle API
def submit_guess():
    global attempt
    if attempt >= 5:
        messagebox.showinfo("Game Over", "You've used all your attempts!")
        return

    guess = guess_entry.get().lower()
    if len(guess) != word_size:
        messagebox.showwarning("Invalid Input", f"Please enter a {word_size}-letter word.")
        return

    feedback = guess_wordle("/random", guess)

    # Clear the entry field
    guess_entry.delete(0, tk.END)

    # Display feedback
    for idx, result in enumerate(feedback['result']):
        color = "gray"  # Default for "absent"
        if result == "correct":
            color = "green"
        elif result == "present":
            color = "yellow"
        letter_label = tk.Label(frame, text=guess[idx].upper(), bg=color, fg="white", width=2, height=1)
        letter_label.grid(row=attempt, column=idx)

    # Check for a win
    if all(result == "correct" for result in feedback['result']):
        messagebox.showinfo("Congratulations", "You guessed the word!")
        reset_game()
        return

    # Increment attempt count
    attempt += 1
    if attempt >= 5:
        messagebox.showinfo("Game Over", "You've used all attempts! Better luck next time.")
        reset_game()


# Function to reset the game
def reset_game():
    global attempt
    attempt = 0
    for widget in frame.winfo_children():
        widget.destroy()

if __name__ == "__main__":
    # guess must be 5 letters long if size not specified
    #response = requests.get(url + "/random", {"guess": "teste", "size": 5, "seed": 0f
    #guess_wordle("/word/", "testray", target="testrat")

  #  response = requests.post(
 #       "https://wordle.votee.dev:8000/wordseg",
  #      data={"text": "example text"}
 #   )
  #  print(response.json())

# need to come up with some gameplay

    if False:
        # Define a word list
        word_list = ["apple", "grape", "peach", "melon", "berry"]

        # Loop to submit guesses
        for attempt in range(10):  # Limit to 10 attempts
            guess = random.choice(word_list)
            feedback = guess_wordle("/random", guess)

            print(f"Attempt {attempt + 1}: Guess: {guess}")
            print(f"Feedback: {feedback}")

            # Check if all results are 'correct'
            if all(r["result"] == "correct" for r in feedback):
                print("Solved the puzzle!")
                break

    attempt = 0
    word_size = 5

    # Initialize the Tkinter window
    root = tk.Tk()
    root.title("Wordle Game")

    # Instructions
    instruction_label = tk.Label(root, text=f"Guess the {word_size}-letter word! You have 5 attempts.", font=("Arial", 14))
    instruction_label.pack(pady=10)

    # Frame for displaying feedback
    frame = tk.Frame(root)
    frame.pack(pady=10)

    # Entry for user's guess
    guess_frame = tk.Frame(root)
    guess_frame.pack(pady=10)

    # Label for entry field
    entry_label = tk.Label(guess_frame, text="Enter your guess:", font=("Arial", 12))
    entry_label.pack(side="left", padx=5)

    # Entry field
    guess_entry = tk.Entry(guess_frame, font=("Arial", 14), justify="center", width=10, bg="lightblue")
    guess_entry.pack(side="left", padx=5)

    # Submit button
    submit_button = tk.Button(guess_frame, text="Submit Guess", font=("Arial", 14), command=submit_guess)
    submit_button.pack(side="left", padx=5)

    # Run the Tkinter event loop
    root.mainloop()

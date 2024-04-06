import random

class NumberGuessingGame:
    def __init__(self):
        self.secret_number = random.randint(1, 101)
        self.attempts = 0

    def guess_number(self, guess):
        self.attempts += 1
        if (self.attempts == 6):
            return "You have used all your attempts"
        if guess < self.secret_number:
            return "Too low! Try again."
        elif guess > self.secret_number:
            return "Too high! Try again."
        else:
            return f"Congratulations! You guessed the number {self.secret_number} in {self.attempts} attempts."

    def reset_game(self):
        self.secret_number = random.randint(1, 100)
        self.attempts = 0
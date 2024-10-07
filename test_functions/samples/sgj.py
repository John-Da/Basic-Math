import random
import time

class MathGame:
    def __init__(self):
        self.running = True
        self.time_limit = 30  # Game runs for 30 seconds
        self.start_time = time.time()

    def addition(self):
        print("Addition problem generated")

    def subtraction(self):
        print("Subtraction problem generated")

    def multiplication(self):
        print("Multiplication problem generated")

    def division(self):
        print("Division problem generated")

    def randomProblems(self):
        """Randomly choose and generate a problem for any operation."""
        operations = ["addition", "subtraction", "multiplication", "division"]
        self.operation = random.choice(operations)

        if self.operation == "addition":
            self.addition()
        elif self.operation == "subtraction":
            self.subtraction()
        elif self.operation == "multiplication":
            self.multiplication()
        elif self.operation == "division":
            self.division()

    def gameLoop(self):
        while self.running:
            current_time = time.time()
            if current_time - self.start_time >= self.time_limit:
                print("Time's up!")
                self.running = False
                break

            self.randomProblems()

            # Add your logic here to check for user input and move to the next problem
            time.sleep(2)  # Simulate a delay before the next problem

# Example usage
game = MathGame()
game.gameLoop()

import random

class MathGame:
    def __init__(self):
        self.operation = None
        self.num1 = 0
        self.num2 = 0
        self.result = 0

    def randomProblems(self):
        operations = ["addition", "subtraction", "multiplication", "division"]
        self.operation = random.choice(operations)
        return self.operation

    def random_operation(self):
        """Randomly select an operation and generate the numbers."""
        self.operation = self.randomProblems()
        if self.operation == 'addition':
            self.addition()
        elif self.operation == 'subtraction':
            self.subtraction()
        elif self.operation == 'multiplication':
            self.multiplication()
        elif self.operation == 'division':
            self.division()
        

            # Generate the next operation after the current one
            # self.operation = random.choice(operations)


    def addition(self):
        """Generate an addition problem."""
        self.num1 = random.randint(1, 100)
        self.num2 = random.randint(1, 100)
        self.result = self.num1 + self.num2
        print(f"Addition: {self.num1} + {self.num2} = ?")

    def subtraction(self):
        """Generate a subtraction problem."""
        self.num1 = random.randint(1, 100)
        self.num2 = random.randint(1, 100)
        self.result = abs(self.num1 - self.num2)  # Keep it positive
        print(f"Subtraction: {self.num1} - {self.num2} = ?")

    def multiplication(self):
        """Generate a multiplication problem."""
        self.num1 = random.randint(1, 100)
        self.num2 = random.randint(1, 100)
        self.result = self.num1 * self.num2
        print(f"Multiplication: {self.num1} * {self.num2} = ?")

    def division(self):
        """Generate a division problem."""
        self.num1 = random.randint(1, 100)
        self.num2 = random.randint(1, 100)
        try:
            if self.num2 != 0:
                self.result = round(self.num1 / self.num2, 2)
                print(f"Division: {self.num1} / {self.num2} = ?")
            else:
                raise ZeroDivisionError("Cannot divide by zero.")
        except ZeroDivisionError as e:
            print(e)
            self.division()  # Retry if division by zero

# Example usage
if __name__ == "__main__":
    game = MathGame()
    i = 6
    while i != 0:
        game.random_operation()
        i -= 1

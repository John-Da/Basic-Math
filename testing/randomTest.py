import random


class Game(object):
    # ... existing code ...

    def random_operation(self):
        """Randomly select an operation for the game"""
        operations = ["addition", "subtraction", "multiplication", "division"]
        self.operation = random.choice(operations)
        self.set_problem()

    def increase_difficulty(self):
        """Increase the difficulty of the game based on the player's score"""
        if self.score > 50:
            self.time_up = 8  # Reduce time for each question
            if self.operation == "addition" or self.operation == "subtraction":
                self.problem["num1"] = random.randint(0, 500)
                self.problem["num2"] = random.randint(0, 500)
            elif self.operation == "multiplication":
                self.problem["num1"] = random.randint(0, 20)
                self.problem["num2"] = random.randint(0, 20)
            elif self.operation == "division":
                divisor = random.randint(1, 20)
                dividend = divisor * random.randint(1, 20)
                self.problem["num1"] = dividend
                self.problem["num2"] = divisor

    def display_stats(self, screen):
        """Display game statistics"""
        stats_font = pygame.font.Font(self.gameFont2, 16)
        accuracy = (self.correct_answers / self.count) * 100 if self.count > 0 else 0
        stats_text = f"Total Questions: {self.count} | Correct: {self.correct_answers} | Accuracy: {accuracy:.1f}%"
        stats_label = stats_font.render(stats_text, True, self.BLACK)
        screen.blit(stats_label, (10, SCREEN_HEIGHT - 30))

    def show_hint(self):
        """Provide a hint for the current problem"""
        hint_text = ""
        if self.operation == "addition":
            hint_text = f"Try adding {self.problem['num1']} and {self.problem['num2']}"
        elif self.operation == "subtraction":
            hint_text = f"Subtract {self.problem['num2']} from {self.problem['num1']}"
        elif self.operation == "multiplication":
            hint_text = f"Multiply {self.problem['num1']} by {self.problem['num2']}"
        elif self.operation == "division":
            hint_text = f"Divide {self.problem['num1']} by {self.problem['num2']}"

        hint_font = pygame.font.Font(self.gameFont2, 18)
        hint_label = hint_font.render(hint_text, True, self.BLACK)
        return hint_label

    def add_power_up(self):
        """Add a power-up button to the game"""
        power_up_button = Button(
            SCREEN_WIDTH - 110, SCREEN_HEIGHT - 60, 100, 50, "Hint"
        )
        return power_up_button

    def process_events(self):
        # ... existing code ...
        if event.type == pygame.MOUSEBUTTONDOWN:
            if not self.show_menu and not self.game_over:
                if self.power_up_button.isPressed():
                    self.show_hint_flag = True
                    self.hint_start_time = pygame.time.get_ticks()
        # ... rest of the existing code ...

    def display_frame(self, screen):
        # ... existing code ...
        if not self.show_menu and not self.game_over:
            # ... existing display code ...
            self.power_up_button.draw(screen)
            if self.show_hint_flag:
                hint_label = self.show_hint()
                screen.blit(
                    hint_label,
                    (
                        SCREEN_WIDTH // 2 - hint_label.get_width() // 2,
                        SCREEN_HEIGHT - 60,
                    ),
                )
                if (
                    pygame.time.get_ticks() - self.hint_start_time > 3000
                ):  # Show hint for 3 seconds
                    self.show_hint_flag = False
            self.display_stats(screen)
        # ... rest of the existing code ...

    def run_logic(self):
        # ... existing code ...
        if not self.show_menu and not self.game_over:
            self.increase_difficulty()
        # ... rest of the existing code ...


# In the main game loop (main.py)
def main():
    # ... existing code ...
    game = Game()
    game.power_up_button = game.add_power_up()
    game.show_hint_flag = False
    game.hint_start_time = 0
    # ... rest of the existing code ...


main()

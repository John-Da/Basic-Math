import os
import pygame
import random



# ------------------------ Requirements -------------------
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

os.chdir(os.path.dirname(os.path.realpath(__file__)))

gameFont1 = "XpressiveBlack Regular.ttf"
gameFont2 = "kenvector_future.ttf"

gameSound1 = "item1.ogg"
gameSound2 = "item2.ogg"

symImage = "symbols.png"
bgImage = "background.jpg"


# ------------------------ Game Section -------------------------

class Game(object):
    def __init__(self):
        # Initialize Fonts
        self.font = pygame.font.SysFont('Arial', 45)  # Changed to use gameFont1
        self.score_font = pygame.font.SysFont('Arial', 20)

        # Initialize Problem and Operation
        self.problem = {"num1": 0, "num2": 0, "result": 0}
        self.operation = ""

        # Load Symbols and Buttons
        self.symbols = self.get_symbols()
        self.button_list = self.get_button_list()
        self.reset_problem = False

        # Initialize Menu
        items = ("Addition", "Subtraction", "Multiplication", "Division", "Random")
        self.menu = Menu(items, ttf_font=gameFont1, font_size=50)
        self.show_menu = True

        # Initialize Game Stats
        self.score = 0
        self.count = 0
        self.correct_answers = 0

        # Load Background Image
        self.background_image = pygame.image.load(bgImage).convert()

        # Load Sounds
        self.sound_1 = pygame.mixer.Sound(gameSound1)
        self.sound_2 = pygame.mixer.Sound(gameSound2)

        # Timer Variables
        self.time_up = 10  # Changed to 60 seconds for longer gameplay
        self.start_time = 0
        self.game_over = False


    def increase_difficulty(self):
        """Increase the difficulty of the game based on the player's correct answers"""
        # **Improvement 3 & 5: Gradual Difficulty Increase and Improved Randomization**
        if self.correct_answers > 0 and self.correct_answers % 5 == 0:
            self.time_up = max(
                10, self.time_up - 2
            )  # Gradually decrease time, not below 10 seconds
            # Gradually increase number ranges
            multiplier = self.correct_answers // 5
            if self.operation in ["addition", "subtraction"]:
                self.problem["num1"] = random.randint(0, 50 * multiplier)
                self.problem["num2"] = random.randint(0, 50 * multiplier)
            elif self.operation == "multiplication":
                self.problem["num1"] = random.randint(0, 12 * multiplier)
                self.problem["num2"] = random.randint(0, 12 * multiplier)
            elif self.operation == "division":
                divisor = random.randint(1, 12 * multiplier)
                dividend = divisor * random.randint(1, 12 * multiplier)
                self.problem["num1"] = dividend
                self.problem["num2"] = divisor


    def get_button_list(self):
        """Return a list with four buttons"""
        button_list = []
        choice = random.randint(1, 4)
        width = 100
        height = 100
        t_w = width * 2 + 50
        posX = (SCREEN_WIDTH / 2) - (t_w / 2)
        posY = 150

        # Create four buttons with one correct answer and three random
        for i in range(4):
            current_choice = i + 1
            if choice == current_choice:
                btn = Button(
                    posX + (i % 2) * 150,
                    posY + (i // 2) * 150,
                    width,
                    height,
                    self.problem["result"],
                )
            else:
                # Ensure random number is not equal to the correct result
                random_number = random.randint(0, 100)
                while random_number == self.problem["result"]:
                    random_number = random.randint(0, 100)
                btn = Button(
                    posX + (i % 2) * 150,
                    posY + (i // 2) * 150,
                    width,
                    height,
                    random_number,
                )
            button_list.append(btn)

        return button_list

    def get_symbols(self):
        """Return a dictionary with all the operation symbols"""
        symbols = {}
        sprite_sheet = pygame.image.load(symImage).convert_alpha() 
        sprite_sheet.set_colorkey(WHITE)
        symbols["addition"] = self.get_image(sprite_sheet, 0, 0, 64, 64)
        symbols["subtraction"] = self.get_image(sprite_sheet, 64, 0, 64, 64)
        symbols["multiplication"] = self.get_image(sprite_sheet, 128, 0, 64, 64)
        symbols["division"] = self.get_image(sprite_sheet, 192, 0, 64, 64)
        
        # Default symbol for random
        symbols["random"] = self.get_image(sprite_sheet, 256, 0, 64, 64)  # Adjust coordinates as needed
        return symbols


    def get_image(self, sprite_sheet, x, y, width, height):
        """This method will cut an image and return it"""
        image = pygame.Surface([width, height], pygame.SRCALPHA).convert_alpha()
        image.blit(sprite_sheet, (0, 0), (x, y, width, height))
        return image

    def addition(self):
        """Set num1, num2, result for addition"""
        self.start_time = pygame.time.get_ticks()

        a = random.randint(0, 100)
        b = random.randint(0, 100)
        self.problem["num1"] = a
        self.problem["num2"] = b
        self.problem["result"] = a + b
        self.operation = "addition"

    def subtraction(self):
        """Set num1, num2, result for subtraction"""
        self.start_time = pygame.time.get_ticks()

        a = random.randint(0, 100)
        b = random.randint(0, 100)
        if a > b:
            self.problem["num1"] = a
            self.problem["num2"] = b
            self.problem["result"] = a - b
        else:
            self.problem["num1"] = b
            self.problem["num2"] = a
            self.problem["result"] = b - a
        self.operation = "subtraction"

    def multiplication(self):
        """Set num1, num2, result for multiplication"""
        self.start_time = pygame.time.get_ticks()

        a = random.randint(0, 12)
        b = random.randint(0, 12)
        self.problem["num1"] = a
        self.problem["num2"] = b
        self.problem["result"] = a * b
        self.operation = "multiplication"

    def division(self):
        """Set num1, num2, result for division"""
        self.start_time = pygame.time.get_ticks()

        divisor = random.randint(1, 12)
        quotient = random.randint(1, 12)
        dividend = divisor * quotient
        self.problem["num1"] = dividend
        self.problem["num2"] = divisor
        self.problem["result"] = quotient
        self.operation = "division"


    def random_operation(self, operation):
        """Randomly select an operation and generate the numbers."""
        try:
            if operation == "addition":
                self.addition()
            elif operation == "subtraction":
                self.subtraction()
            elif operation == "multiplication":
                self.multiplication()
            elif operation == "division":
                self.division()

        except Exception as e:
            print(f"Error: {e}")

            

    def check_result(self):
        """Check the result when a button is pressed"""
        for button in self.button_list:
            if button.isPressed():
                if button.get_number() == self.problem["result"]:
                    button.set_color(GREEN)
                    self.score += 5
                    self.correct_answers += 1
                    self.sound_1.play()
                else:
                    button.set_color(RED)
                    self.sound_2.play()
                self.reset_problem = True



    def process_events(self):
        """Handle all incoming events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                os._exit(1)
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if not self.show_menu and not self.game_over:
                    self.check_result()
                elif self.show_menu:  # Handle menu selection
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        # Ensure that menu state is updated before setting the operation
                        self.menu.update()
                        if self.menu.state == 0:  # Addition
                            self.operation = "addition"
                        elif self.menu.state == 1:  # Subtraction
                            self.operation = "subtraction"
                        elif self.menu.state == 2:  # Multiplication
                            self.operation = "multiplication"
                        elif self.menu.state == 3:  # Division
                            self.operation = "division"
                        elif self.menu.state == 4:  # Random
                            self.operation = "random"
                            self.show_menu = False
                            self.start_time = pygame.time.get_ticks()  # Start the timer
                            return
                        
                        # Set up a new problem based on the selected operation
                        self.set_problem()
                        self.show_menu = False
                        self.start_time = pygame.time.get_ticks()  # Start the timer

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE and not self.game_over:
                    self.show_menu = True
                    self.score = 0
                    self.count = 0
                    self.correct_answers = 0
                    self.game_over = False
                    self.time_up = 10  # Reset timer to original value

                if self.game_over and event.key == pygame.K_RETURN:
                    self.show_menu = True
                    self.score = 0
                    self.count = 0
                    self.correct_answers = 0
                    self.game_over = False
                    self.time_up = 10  # Reset timer to original value

        return False

    def set_problem(self):
        """Set up a new problem based on the current operation."""
        if self.operation == "random":  # Check if random mode is selected
            self.randomProblems()  # Randomly choose and set an operation
            # Call the specific method based on the operation
        elif self.operation == "addition":
            self.addition()
        elif self.operation == "subtraction":
            self.subtraction()
        elif self.operation == "multiplication":
            self.multiplication()
        elif self.operation == "division":
            self.division()
        
        # Re-generate the answer buttons with the new problem
        self.button_list = self.get_button_list()

    def randomProblems(self):
        """Randomly choose and generate a problem for any operation."""
        operations = ["addition", "subtraction", "multiplication", "division"]
        chosen_operation = random.choice(operations)  # Randomly choose an operation
        self.random_operation(chosen_operation)


    def run_logic(self):
        """Run the game's logic"""
        if not self.show_menu and not self.game_over:
            self.increase_difficulty()
        self.menu.update()

    def display_message(self, screen, items):
        """Display messages on the screen"""
        for index, message in enumerate(items):
            label = self.font.render(message, True, BLACK)
            width = label.get_width()
            height = label.get_height()

            posX = (SCREEN_WIDTH / 2) - (width / 2)
            t_h = len(items) * height
            posY = (SCREEN_HEIGHT / 2) - (t_h / 2) + (index * height)

            screen.blit(label, (posX, posY))

    def display_frame(self, screen):
        """Draw everything on the screen"""
        screen.blit(self.background_image, (0, 0))
        time_wait = False

        if self.show_menu:
            self.menu.display_frame(screen)
        elif self.game_over:
            msg_1 = f"You answered {self.correct_answers} correctly"
            msg_2 = f"Your score was {self.score}"
            msg_3 = "Press Enter to Restart"

            # Display Game Over Messages
            self.display_message(screen, (msg_1, msg_2))
            label = self.score_font.render(msg_3, True, BLACK)
            width = label.get_width()
            height = label.get_height()

            posX = (SCREEN_WIDTH / 2) - (width / 2)
            posY = (SCREEN_HEIGHT / 2) + 60

            screen.blit(label, (posX, posY))
            time_wait = True

        if not self.show_menu and not self.game_over:


            # Display Problem and Buttons
            label_1 = self.font.render(str(self.problem["num1"]), True, BLACK)
            label_2 = self.font.render(str(self.problem["num2"]) + " = ?", True, BLACK)
            t_w = label_1.get_width() + label_2.get_width() + 64  # 64: length of symbol
            posX = (SCREEN_WIDTH / 2) - (t_w / 2)
            screen.blit(label_1, (posX, 50))
            screen.blit(self.symbols[self.operation], (posX + label_1.get_width(), 40))
            screen.blit(label_2, (posX + label_1.get_width() + 64, 50))

            # Draw Buttons
            for btn in self.button_list:
                btn.draw(screen)

            # Display Score and Timer
            score_label = self.score_font.render(
                "Score: " + str(self.score), True, WHITE
            )
            timer_label = self.display_timer()
            screen.blit(score_label, (10, 10))
            screen.blit(timer_label, (SCREEN_WIDTH - timer_label.get_width() - 40, 10))

        pygame.display.flip()

        if self.reset_problem:
            pygame.time.wait(1000)
            self.set_problem()
            self.count += 1
            self.reset_problem = False
        elif time_wait:
            pygame.time.wait(3000)

    def display_timer(self):
        """Display the remaining time"""
        elapsed_time = (pygame.time.get_ticks() - self.start_time) // 1000
        remaining_time = self.time_up - elapsed_time

        if remaining_time <= 0 and not self.game_over:
            self.game_over = True
            remaining_time = 0

        minutes = str(remaining_time // 60).zfill(2)
        seconds = str(remaining_time % 60).zfill(2)
        timer_text = (
            f"{minutes}:{seconds}"  # **Improvement 4: Clear Timer Label**
        )

        return self.score_font.render(timer_text, True, WHITE)



# --------------------------- Button Section ------------------------


class Button(object):
    def __init__(self, x, y, width, height, number):
        self.rect = pygame.Rect(x, y, width, height)
        self.font = pygame.font.Font(None, 40)
        self.text = self.font.render(str(number), True, BLACK)
        self.number = number
        self.background_color = WHITE

    def draw(self, screen):
        """Draw the button to the screen"""
        pygame.draw.rect(screen, self.background_color, self.rect)
        pygame.draw.rect(screen, BLACK, self.rect, 3)
        width = self.text.get_width()
        height = self.text.get_height()
        posX = self.rect.centerx - (width / 2)
        posY = self.rect.centery - (height / 2)
        screen.blit(self.text, (posX, posY))

    def isPressed(self):
        """Return True if the mouse is on the button and clicked."""
        pos = pygame.mouse.get_pos()
        return self.rect.collidepoint(pos)

    def set_color(self, color):
        """Set the background color"""
        self.background_color = color

    def get_number(self):
        """Return the number of the button."""
        return self.number


# -------------------------- Menu Section --------------------

class Menu(object):
    state = -1

    def __init__(
        self,
        items,
        font_color=(0, 0, 0),
        select_color=(255, 0, 0),
        ttf_font=None,
        font_size=25,
    ):
        self.font_color = font_color
        self.select_color = select_color
        self.items = items
        self.font = pygame.font.Font(ttf_font, font_size)
        # Generate a list that will contain the rect for each item
        self.rect_list = self.get_rect_list(items)

    def get_rect_list(self, items):
        rect_list = []
        for index, item in enumerate(items):
            # determine the amount of space needed to render text
            size = self.font.size(item)
            # Get the width and height of the text
            width = size[0]
            height = size[1]

            posX = (SCREEN_WIDTH / 2) - (width / 2)
            # t_h: total heigth of the text block
            t_h = len(items) * height
            posY = (SCREEN_HEIGHT / 2) - (t_h / 2) + (index * height)
            # Create rects
            rect = pygame.Rect(posX, posY, width, height)
            # Add rect to the list
            rect_list.append(rect)

        return rect_list

    def collide_points(self):
        index = -1
        mouse_pos = pygame.mouse.get_pos()
        for i, rect in enumerate(self.rect_list):
            if rect.collidepoint(mouse_pos):
                index = i

        return index

    def update(self):
        # assign collide_points to state
        self.state = self.collide_points()

    def display_frame(self, screen):
        for index, item in enumerate(self.items):
            if self.state == index:
                label = self.font.render(item, True, self.select_color)
            else:
                label = self.font.render(item, True, self.font_color)

            width = label.get_width()
            height = label.get_height()

            posX = (SCREEN_WIDTH / 2) - (width / 2)
            # t_h: total height of text block
            t_h = len(self.items) * height
            posY = (SCREEN_HEIGHT / 2) - (t_h / 2) + (index * height)

            screen.blit(label, (posX, posY))


def main():
    pygame.init()
    pygame.mixer.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
    pygame.display.set_caption("Basic Math")
    done = False
    clock = pygame.time.Clock()
    game = Game()
    while not done:
        done = game.process_events()
        game.run_logic()
        game.display_frame(screen)
        clock.tick(60)
    pygame.quit()


if __name__ == "__main__":
    main()
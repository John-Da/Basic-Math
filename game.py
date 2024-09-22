import pygame, random
import os
from menu import Menu

SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480

# Colors
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


class Game(object):
    def __init__(self):
        self.font = pygame.font.Font(None, 65)
        self.score_font = pygame.font.Font(gameFont2, 20)
        self.problem = {"num1": 0, "num2": 0, "result": 0}
        self.operation = ""
        self.symbols = self.get_symbols()
        self.button_list = self.get_button_list()
        self.reset_problem = False
        items = ("Addition", "Subtraction", "Multiplication", "Division")
        self.menu = Menu(items, ttf_font=gameFont1, font_size=50)
        self.show_menu = True
        self.score = 0
        self.count = 0
        self.background_image = pygame.image.load(bgImage).convert()
        self.sound_1 = pygame.mixer.Sound(gameSound1)
        self.sound_2 = pygame.mixer.Sound(gameSound2)

        self.time_up = 60

    def get_button_list(self):
        """Return a list with four buttons"""
        button_list = []
        choice = random.randint(1, 4)
        width = 100
        height = 100
        t_w = width * 2 + 50
        posX = (SCREEN_WIDTH / 2) - (t_w / 2)
        posY = 150
        if choice == 1:
            btn = Button(posX, posY, width, height, self.problem["result"])
            button_list.append(btn)
        else:
            btn = Button(posX, posY, width, height, random.randint(0, 100))
            button_list.append(btn)

        posX = (SCREEN_WIDTH / 2) - (t_w / 2) + 150

        if choice == 2:
            btn = Button(posX, posY, width, height, self.problem["result"])
            button_list.append(btn)
        else:
            btn = Button(posX, posY, width, height, random.randint(0, 100))
            button_list.append(btn)

        posX = (SCREEN_WIDTH / 2) - (t_w / 2)
        posY = 300

        if choice == 3:
            btn = Button(posX, posY, width, height, self.problem["result"])
            button_list.append(btn)
        else:
            btn = Button(posX, posY, width, height, random.randint(0, 100))
            button_list.append(btn)

        posX = (SCREEN_WIDTH / 2) - (t_w / 2) + 150

        if choice == 4:
            btn = Button(posX, posY, width, height, self.problem["result"])
            button_list.append(btn)
        else:
            btn = Button(posX, posY, width, height, random.randint(0, 100))
            button_list.append(btn)

        return button_list

    def get_symbols(self):
        """Return a dictionary with all the operation symbols"""
        symbols = {}
        sprite_sheet = pygame.image.load(symImage).convert()
        image = self.get_image(sprite_sheet, 0, 0, 64, 64)
        symbols["addition"] = image
        image = self.get_image(sprite_sheet, 64, 0, 64, 64)
        symbols["subtraction"] = image
        image = self.get_image(sprite_sheet, 128, 0, 64, 64)
        symbols["multiplication"] = image
        image = self.get_image(sprite_sheet, 192, 0, 64, 64)
        symbols["division"] = image

        return symbols

    def get_image(self, sprite_sheet, x, y, width, height):
        """This method will cut an image and return it"""
        image = pygame.Surface([width, height]).convert()
        image.blit(sprite_sheet, (0, 0), (x, y, width, height))
        return image

    def addition(self):
        """These will set num1,num2,result for addition"""
        a = random.randint(0, 100)
        b = random.randint(0, 100)
        self.problem["num1"] = a
        self.problem["num2"] = b
        self.problem["result"] = a + b
        self.operation = "addition"

    def subtraction(self):
        """These will set num1,num2,result for subtraction"""
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
        """These will set num1,num2,result for multiplication"""
        a = random.randint(0, 12)
        b = random.randint(0, 12)
        self.problem["num1"] = a
        self.problem["num2"] = b
        self.problem["result"] = a * b
        self.operation = "multiplication"

    def division(self):
        """These will set num1,num2,result for division"""
        divisor = random.randint(1, 12)
        dividend = divisor * random.randint(1, 12)
        quotient = dividend / divisor
        self.problem["num1"] = dividend
        self.problem["num2"] = divisor
        self.problem["result"] = quotient
        self.operation = "division"

    def check_result(self):
        """Check the result"""
        for button in self.button_list:
            if button.isPressed():
                if button.get_number() == self.problem["result"]:
                    button.set_color(GREEN)
                    self.score += 5
                    self.sound_1.play()
                else:
                    button.set_color(RED)
                    self.sound_2.play()
                self.reset_problem = True

    def set_problem(self):
        """do another problem again"""
        if self.operation == "addition":
            self.addition()
        elif self.operation == "subtraction":
            self.subtraction()
        elif self.operation == "multiplication":
            self.multiplication()
        elif self.operation == "division":
            self.division()
        self.button_list = self.get_button_list()

    def process_events(self):
        for event in pygame.event.get():  
            if event.type == pygame.QUIT:  
                return True
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.show_menu:
                    if self.menu.state == 0:
                        self.operation = "addition"
                        self.set_problem()
                        self.show_menu = False
                    elif self.menu.state == 1:
                        self.operation = "subtraction"
                        self.set_problem()
                        self.show_menu = False
                    elif self.menu.state == 2:
                        self.operation = "multiplication"
                        self.set_problem()
                        self.show_menu = False
                    elif self.menu.state == 3:
                        self.operation = "division"
                        self.set_problem()
                        self.show_menu = False

                else:
                    self.check_result()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.show_menu = True
                    self.score = 0
                    self.count = 0

        return False

    def run_logic(self):
        self.menu.update()

    def display_message(self, screen, items):
        """display every string that is inside of a tuple(args)"""
        for index, message in enumerate(items):
            label = self.font.render(message, True, BLACK)
            width = label.get_width()
            height = label.get_height()

            posX = (SCREEN_WIDTH / 2) - (width / 2)
            t_h = len(items) * height
            posY = (SCREEN_HEIGHT / 2) - (t_h / 2) + (index * height)

            screen.blit(label, (posX, posY))

    def display_frame(self, screen):
        screen.blit(self.background_image, (0, 0))
        time_wait = False
        if self.show_menu:
            self.menu.display_frame(screen)
        elif self.count == 20:
            msg_1 = "You answered " + str(self.score / 5) + " correctly"
            msg_2 = "Your score was " + str(self.score)
            self.display_message(screen, (msg_1, msg_2))
            self.show_menu = True
            self.score = 0
            self.count = 0
            time_wait = True
        else:
            label_1 = self.font.render(str(self.problem["num1"]), True, BLACK)
            label_2 = self.font.render(str(self.problem["num2"]) + " = ?", True, BLACK)
            t_w = label_1.get_width() + label_2.get_width() + 64  # 64: length of symbol
            posX = (SCREEN_WIDTH / 2) - (t_w / 2)
            screen.blit(label_1, (posX, 50))
            screen.blit(self.symbols[self.operation], (posX + label_1.get_width(), 40))

            screen.blit(label_2, (posX + label_1.get_width() + 64, 50))
            for btn in self.button_list:
                btn.draw(screen)
            score_label = self.score_font.render(
                "Score: " + str(self.score), True, BLACK
            )
            screen.blit(score_label, (10, 10))

        pygame.display.flip()
        if self.reset_problem:
            pygame.time.wait(1000)
            self.set_problem()
            self.count += 1
            self.reset_problem = False
        elif time_wait:
            pygame.time.wait(3000)

    
    def display_timer(self):
        self.count_time = pygame.time.get_ticks()

        minutes = str(self.count_time // 60000).zfill(2)
        seconds = str(self.time_up - ((self.count_time % 60000) // 1000)).zfill(2)

        displayTime = "%s:%s" % (
            minutes,
            seconds
        )


class Button(object):
    def __init__(self, x, y, width, height, number):
        self.rect = pygame.Rect(x, y, width, height)
        self.font = pygame.font.Font(None, 40)
        self.text = self.font.render(str(number), True, BLACK)
        self.number = number
        self.background_color = WHITE

    def draw(self, screen):
        """This method will draw the button to the screen"""
        pygame.draw.rect(screen, self.background_color, self.rect)
        pygame.draw.rect(screen, BLACK, self.rect, 3)
        width = self.text.get_width()
        height = self.text.get_height()
        posX = self.rect.centerx - (width / 2)
        posY = self.rect.centery - (height / 2)
        screen.blit(self.text, (posX, posY))

    def isPressed(self):
        """Return true if the mouse is on the button"""
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            return True
        else:
            return False

    def set_color(self, color):
        """Set the background color"""
        self.background_color = color

    def get_number(self):
        """Return the number of the button."""
        return self.number

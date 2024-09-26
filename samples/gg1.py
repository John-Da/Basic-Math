import sys
import os
import random
import time
from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QLineEdit,
    QHBoxLayout,
    QComboBox,
    QGridLayout,
)
from PyQt6.QtCore import QTimer
from PyQt6.QtGui import QFont, QPixmap


os.chdir(os.path.dirname(os.path.realpath(__file__)))


class SpeedMathGame(QWidget):
    def __init__(self):
        super().__init__()

        # Game state variables
        self.num1 = 0
        self.num2 = 0
        self.score = 0
        self.time_limit = 60  # 60 seconds to play
        self.start_time = 0
        self.operation = "+"
        self.difficulty = "Medium"

        # UI setup
        self.initUI()

        # Timer
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_timer)

    def initUI(self):
        # Background image
        self.setStyleSheet(
            """
            QWidget {
                background-image: url('background.jpg');
                background-repeat: no-repeat;
                background-position: center;
            }
            """
        )

        # Set up main layout
        self.main_layout = QVBoxLayout()

        # Title Section
        self.title_label = QLabel("Speed Math Game")
        self.title_label.setFont(QFont("Arial", 30, QFont.Weight.Bold))
        self.title_label.setStyleSheet("color: #5C0A9B;")
        self.main_layout.addWidget(self.title_label)

        # Difficulty and Operation Section
        self.selector_layout = QHBoxLayout()

        # Dropdown for difficulty selection
        self.difficulty_selector = QComboBox(self)
        self.difficulty_selector.addItems(["Easy", "Medium", "Hard"])
        self.difficulty_selector.setFont(QFont("Arial", 18))
        self.selector_layout.addWidget(QLabel("Difficulty: "))
        self.selector_layout.addWidget(self.difficulty_selector)

        self.main_layout.addLayout(self.selector_layout)

        # Game Play Layout
        self.game_layout = QVBoxLayout()

        # Question label
        self.question_label = QLabel("2 + 3")
        self.question_label.setFont(QFont("Arial", 40))
        self.question_label.setStyleSheet("color: #5C0A9B;")
        self.game_layout.addWidget(self.question_label)

        # Answer buttons in grid layout
        self.grid_layout = QGridLayout()
        self.buttons = []
        for i in range(6):  # 6 number choices
            btn = QPushButton(str(i + random.randint(1, 10)), self)
            btn.setFont(QFont("Arial", 22))
            btn.setFixedSize(100, 100)
            btn.setStyleSheet(
                "background-color: #F95A5A; color: white; border-radius: 20px;"
            )
            btn.clicked.connect(self.check_answer)
            self.grid_layout.addWidget(
                btn, i // 3, i % 3
            )  # Organize buttons in a 2x3 grid
            self.buttons.append(btn)

        self.game_layout.addLayout(self.grid_layout)

        # Start Button
        self.start_button = QPushButton("Start", self)
        self.start_button.setFont(QFont("Arial", 22))
        self.start_button.setStyleSheet(
            "background-color: #F95A5A; color: white; border-radius: 10px;"
        )
        self.start_button.clicked.connect(self.start_game)
        self.game_layout.addWidget(self.start_button)

        self.main_layout.addLayout(self.game_layout)

        self.setLayout(self.main_layout)
        self.setWindowTitle("Speed Math Game")
        self.setGeometry(100, 100, 520, 800)

    def start_game(self):
        # Reset game state
        self.score = 0
        self.time_limit = 60
        self.start_time = time.time()
        self.generate_question()

        # Get selected difficulty
        self.difficulty = self.difficulty_selector.currentText()

        # Start the timer
        self.timer.start(1000)

    def generate_question(self):
        # Generate random numbers based on difficulty level
        if self.difficulty == "Easy":
            self.num1 = random.randint(1, 10)
            self.num2 = random.randint(1, 10)
        elif self.difficulty == "Medium":
            self.num1 = random.randint(10, 50)
            self.num2 = random.randint(10, 50)
        else:  # Hard difficulty
            self.num1 = random.randint(50, 100)
            self.num2 = random.randint(50, 100)

        self.question_label.setText(f"{self.num1} + {self.num2}")
        self.update_answer_buttons()

    def update_answer_buttons(self):
        # Randomly place the correct answer and other options on the buttons
        correct_answer = self.num1 + self.num2
        correct_btn_index = random.randint(0, 5)
        for i, btn in enumerate(self.buttons):
            if i == correct_btn_index:
                btn.setText(str(correct_answer))
            else:
                btn.setText(str(correct_answer + random.randint(-10, 10)))

    def check_answer(self):
        sender = self.sender()
        if sender.text() == str(self.num1 + self.num2):
            self.score += 1
            self.generate_question()
        else:
            self.score -= 1  # Optional: you can deduct points for wrong answers

    def update_timer(self):
        elapsed_time = time.time() - self.start_time
        time_left = self.time_limit - int(elapsed_time)

        if time_left <= 0:
            self.timer.stop()
            self.question_label.setText(f"Game Over! Final Score: {self.score}")
            self.start_button.setDisabled(False)
            for btn in self.buttons:
                btn.setDisabled(True)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    game = SpeedMathGame()
    game.show()
    sys.exit(app.exec())

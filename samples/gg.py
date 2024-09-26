import sys
import random
import time
from PyQt6.QtWidgets import (QApplication, QWidget, QLabel, QPushButton, 
                             QVBoxLayout, QLineEdit, QHBoxLayout, QComboBox)
from PyQt6.QtCore import QTimer
from PyQt6.QtGui import QFont

class SpeedMathGame(QWidget):
    def __init__(self):
        super().__init__()
        
        # Game state variables
        self.num1 = 0
        self.num2 = 0
        self.score = 0
        self.time_limit = 60  # 60 seconds to play
        self.start_time = 0
        self.operation = '+'
        self.difficulty = 'Easy'
        
        # UI setup
        self.initUI()
        
        # Timer
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_timer)
        
    def initUI(self):
        # Set up main layout
        self.layout = QVBoxLayout()
        
        # Title Label
        self.title_label = QLabel('Speed Math Game')
        self.title_label.setFont(QFont('Arial', 24))
        self.layout.addWidget(self.title_label)
        
        # Question Label
        self.question_label = QLabel('Solve: ')
        self.question_label.setFont(QFont('Arial', 18))
        self.layout.addWidget(self.question_label)
        
        # Score Label
        self.score_label = QLabel(f'Score: {self.score}')
        self.layout.addWidget(self.score_label)
        
        # Timer Label
        self.timer_label = QLabel(f'Time left: {self.time_limit}')
        self.layout.addWidget(self.timer_label)
        
        # Input field for answer
        self.answer_input = QLineEdit(self)
        self.answer_input.setPlaceholderText('Enter your answer')
        self.answer_input.returnPressed.connect(self.check_answer)
        self.layout.addWidget(self.answer_input)
        
        # Horizontal layout for operation and difficulty
        h_layout = QHBoxLayout()

        # Dropdown for operation selection
        self.operation_selector = QComboBox(self)
        self.operation_selector.addItems(['+', '-', '*', '/'])
        h_layout.addWidget(QLabel('Operation:'))
        h_layout.addWidget(self.operation_selector)

        # Dropdown for difficulty selection
        self.difficulty_selector = QComboBox(self)
        self.difficulty_selector.addItems(['Easy', 'Medium', 'Hard'])
        h_layout.addWidget(QLabel('Difficulty:'))
        h_layout.addWidget(self.difficulty_selector)
        
        self.layout.addLayout(h_layout)
        
        # Start button
        self.start_button = QPushButton('Start Game', self)
        self.start_button.setStyleSheet('background-color: green; color: white; font-size: 16px;')
        self.start_button.clicked.connect(self.start_game)
        self.layout.addWidget(self.start_button)
        
        # Set layout and window title
        self.setLayout(self.layout)
        self.setWindowTitle('Speed Math Game')
        self.setGeometry(100, 100, 400, 300)
        
    def start_game(self):
        # Reset game state
        self.score = 0
        self.update_score()
        self.time_limit = 60
        self.start_time = time.time()
        self.update_timer_label()
        self.generate_question()
        
        # Get selected operation and difficulty
        self.operation = self.operation_selector.currentText()
        self.difficulty = self.difficulty_selector.currentText()
        
        # Start the timer
        self.timer.start(1000)
        
    def generate_question(self):
        # Generate random numbers based on difficulty level
        if self.difficulty == 'Easy':
            self.num1 = random.randint(1, 10)
            self.num2 = random.randint(1, 10)
        elif self.difficulty == 'Medium':
            self.num1 = random.randint(10, 50)
            self.num2 = random.randint(10, 50)
        else:  # Hard difficulty
            self.num1 = random.randint(50, 100)
            self.num2 = random.randint(50, 100)
        
        # Avoid division by zero
        if self.operation == '/' and self.num2 == 0:
            self.num2 = random.randint(1, 10)
        
        # Update question label based on operation
        self.question_label.setText(f'Solve: {self.num1} {self.operation} {self.num2}')
        
    def check_answer(self):
        user_answer = self.answer_input.text()
        
        try:
            # Calculate correct answer based on selected operation
            correct_answer = 0
            if self.operation == '+':
                correct_answer = self.num1 + self.num2
            elif self.operation == '-':
                correct_answer = self.num1 - self.num2
            elif self.operation == '*':
                correct_answer = self.num1 * self.num2
            elif self.operation == '/':
                correct_answer = round(self.num1 / self.num2, 2)
            
            # Check if user answer is correct
            if float(user_answer) == correct_answer:
                self.score += 1
                self.update_score()
        except ValueError:
            pass  # Ignore if the input is not a valid number
        
        self.answer_input.clear()
        self.generate_question()
        
    def update_score(self):
        self.score_label.setText(f'Score: {self.score}')
        
    def update_timer(self):
        elapsed_time = time.time() - self.start_time
        time_left = self.time_limit - int(elapsed_time)
        self.update_timer_label(time_left)
        
        if time_left <= 0:
            self.timer.stop()
            self.question_label.setText(f'Game Over! Final Score: {self.score}')
            self.answer_input.setDisabled(True)
            self.start_button.setDisabled(False)
        
    def update_timer_label(self, time_left=None):
        if time_left is None:
            time_left = self.time_limit
        self.timer_label.setText(f'Time left: {time_left}')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    game = SpeedMathGame()
    game.show()
    sys.exit(app.exec())
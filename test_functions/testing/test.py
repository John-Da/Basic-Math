import pygame
import time

# Initialize Pygame
pygame.init()

# Set up display
screen = pygame.display.set_mode((600, 400))
pygame.display.set_caption('Math Game with Timer')

# Font
font = pygame.font.Font(None, 36)

# Timer settings (in milliseconds)
total_time = 60000  # 60 seconds
start_ticks = pygame.time.get_ticks()  # Get starting time

# Game variables
score = 0
correct_answers = 0
game_over = False

# Example of a game loop
running = True
while running:
    # Clear the screen
    screen.fill((255, 255, 255))

    # Check for quit event
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Timer logic
    elapsed_time = pygame.time.get_ticks() - start_ticks
    remaining_time = total_time - elapsed_time

    # Display timer
    timer_text = font.render(f"Time left: {remaining_time // 1000}s", True, (0, 0, 0))
    screen.blit(timer_text, (10, 10))

    # Game over logic
    if remaining_time <= 0:
        game_over = True

    if not game_over:
        # Game logic, e.g., displaying questions and checking answers
        # (Add your addition, multiplication logic here)

        # Example score and correct answers calculation
        score += 1
        correct_answers += 1
    else:
        # Display game over screen with score and correct answers
        game_over_text = font.render(f"Game Over!", True, (255, 0, 0))
        score_text = font.render(f"Score: {score}", True, (0, 0, 0))
        correct_text = font.render(f"Correct Answers: {correct_answers}", True, (0, 0, 0))
        screen.blit(game_over_text, (200, 150))
        screen.blit(score_text, (200, 200))
        screen.blit(correct_text, (200, 250))

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()

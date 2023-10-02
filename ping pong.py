import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 1920, 1080  # Updated resolution
BALL_SPEED = 7  # Increased default ball speed
PADDLE_SPEED = 10

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Game states
MAIN_MENU = 0
GAME_PLAYING = 1
GAME_OVER = 2  # Added GAME_OVER state

# Create the game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong Game")

# Paddle dimensions
PADDLE_WIDTH, PADDLE_HEIGHT = 10, 100

# Create paddles
player_paddle = pygame.Rect(50, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
opponent_paddle = pygame.Rect(WIDTH - 50 - PADDLE_WIDTH, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)

# Create the ball
ball = pygame.Rect(WIDTH // 2 - 15, HEIGHT // 2 - 15, 30, 30)

# Initialize ball_speed_x and ball_speed_y as global variables
ball_speed_x = BALL_SPEED * random.choice((1, -1))
ball_speed_y = BALL_SPEED * random.choice((1, -1))

# AI opponent's speed and skill level
ai_speed = 10  # Increased AI speed
ai_skill = 0.9  # Improved default AI skill

# Game state, difficulty, and score
game_state = MAIN_MENU
difficulty = None
score = 0  # Added score variable

def reset_game():
    global game_state, ball_speed_x, ball_speed_y, score
    ball.center = (WIDTH // 2, HEIGHT // 2)
    ball_speed_x = BALL_SPEED * random.choice((1, -1))
    ball_speed_y = BALL_SPEED * random.choice((1, -1))
    game_state = GAME_PLAYING
    score = 0

def move_opponent_paddle(target_y):
    if opponent_paddle.centery < target_y:
        opponent_paddle.centery += ai_speed * ai_skill
    elif opponent_paddle.centery > target_y:
        opponent_paddle.centery -= ai_speed * ai_skill

def increase_ball_speed(difficulty):
    global ball_speed_x, ball_speed_y, ai_skill
    if difficulty == "Extremely Easy":
        ai_skill = 0.4
        ball_speed_x *= 0.5
        ball_speed_y *= 0.5
    elif difficulty == "Easy":
        ai_skill = 0.6
        ball_speed_x *= 0.7
        ball_speed_y *= 0.7
    elif difficulty == "Medium":
        ai_skill = 0.7
    elif difficulty == "Hard":
        ai_skill = 0.8
        ball_speed_x *= 1.3
        ball_speed_y *= 1.3
    elif difficulty == "Hardcore":
        ai_skill = 1.0
        ball_speed_x *= 1.5
        ball_speed_y *= 1.5
    elif difficulty == "Hacker":
        ai_skill = 1.6
        ball_speed_x *= 2
        ball_speed_y *= 2

def main_menu():
    global game_state, difficulty

    while game_state == MAIN_MENU:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if difficulty:
                        reset_game()
                        increase_ball_speed(difficulty)
                    else:
                        print("Please select a difficulty first.")
                elif event.key == pygame.K_UP:
                    if difficulty == "Extremely Easy":
                        difficulty = "Hacker"
                    elif difficulty:
                        difficulties = ["Extremely Easy", "Easy", "Medium", "Hard", "Hardcore", "Hacker"]
                        idx = difficulties.index(difficulty)
                        difficulty = difficulties[idx - 1]
                    else:
                        difficulty = "Hacker"
                elif event.key == pygame.K_DOWN:
                    if difficulty == "Hacker":
                        difficulty = "Extremely Easy"
                    elif difficulty:
                        difficulties = ["Extremely Easy", "Easy", "Medium", "Hard", "Hardcore", "Hacker"]
                        idx = difficulties.index(difficulty)
                        if idx < len(difficulties) - 1:
                            difficulty = difficulties[idx + 1]
                    else:
                        difficulty = "Extremely Easy"

        # Clear the screen
        screen.fill(BLACK)

        # Draw main menu text
        font = pygame.font.Font(None, 72)
        title_text = font.render("Pong Game", True, WHITE)
        start_text = font.render("Press ENTER to Start", True, WHITE)
        diff_text = font.render("Difficulty: " + (difficulty or "Select Difficulty"), True, WHITE)
        up_down_text = font.render("Use UP/DOWN arrows to change difficulty", True, WHITE)
        screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, 300))
        screen.blit(start_text, (WIDTH // 2 - start_text.get_width() // 2, 500))
        screen.blit(diff_text, (WIDTH // 2 - diff_text.get_width() // 2, 650))
        screen.blit(up_down_text, (WIDTH // 2 - up_down_text.get_width() // 2, 750))

        # Update the display
        pygame.display.flip()

def main_game():
    global game_state, ball_speed_x, ball_speed_y, score  # Declare them as global

    while game_state == GAME_PLAYING:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and player_paddle.top > 0:
            player_paddle.y -= PADDLE_SPEED
        if keys[pygame.K_DOWN] and player_paddle.bottom < HEIGHT:
            player_paddle.y += PADDLE_SPEED

        # AI opponent tracks the ball's position
        move_opponent_paddle(ball.y)

        # Update ball position
        ball.x += ball_speed_x
        ball.y += ball_speed_y

        # Ball collision with paddles
        if ball.colliderect(player_paddle) or ball.colliderect(opponent_paddle):
            ball_speed_x *= -1

        # Ball collision with top and bottom walls
        if ball.top <= 0 or ball.bottom >= HEIGHT:
            ball_speed_y *= -1

        # Game over condition
        if ball.left <= 0:
            game_state = GAME_OVER
            score = 0  # Reset score on game over
        elif ball.right >= WIDTH:
            game_state = GAME_OVER
            score = 1  # Set score to 1 (win) on game over

        # Clear the screen
        screen.fill(BLACK)

        # Draw paddles and ball
        pygame.draw.rect(screen, WHITE, player_paddle)
        pygame.draw.rect(screen, WHITE, opponent_paddle)
        pygame.draw.ellipse(screen, WHITE, ball)

        # Update the display
        pygame.display.flip()

        # Control the game speed
        pygame.time.Clock().tick(60)

def game_over():
    global game_state, score

    while game_state == GAME_OVER:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    game_state = MAIN_MENU  # Return to the main menu on Enter key press

        # Clear the screen
        screen.fill(BLACK)

        # Draw game over text
        font = pygame.font.Font(None, 72)
        game_over_text = font.render("Game Over", True, WHITE)
        score_text = font.render("Score: " + ("Win" if score == 1 else "Lose"), True, WHITE)
        restart_text = font.render("Press ENTER to return to the main menu", True, WHITE)
        screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, 300))
        screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, 500))
        screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, 650))

        # Update the display
        pygame.display.flip()

if __name__ == "__main__":
    while True:
        if game_state == MAIN_MENU:
            main_menu()
        elif game_state == GAME_PLAYING:
            main_game()
        elif game_state == GAME_OVER:
            game_over()

import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = pygame.display.Info().current_w, pygame.display.Info().current_h
BALL_SPEED = 7
PADDLE_SPEED = 10

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Game states
MAIN_MENU = 0
GAME_PLAYING = 1
GAME_OVER = 2

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

# Initialize ball speed
ball_speed = [BALL_SPEED * random.choice((1, -1)), BALL_SPEED * random.choice((1, -1))]

# AI opponent's speed and skill level
ai_speed = 10
ai_skill = 0.9

# Game state, difficulty, and score
game_state = MAIN_MENU
difficulty_levels = {
    "Extremely Easy": {"ai_skill": 0.4, "ball_speed_multiplier": 0.5},
    "Easy": {"ai_skill": 0.6, "ball_speed_multiplier": 0.7},
    "Medium": {"ai_skill": 0.7, "ball_speed_multiplier": 1.0},
    "Hard": {"ai_skill": 0.8, "ball_speed_multiplier": 1.3},
    "Hardcore": {"ai_skill": 1.0, "ball_speed_multiplier": 1.5},
    "Hacker": {"ai_skill": 1.6, "ball_speed_multiplier": 2.0},
}
selected_difficulty = None
score = 0

def reset_game():
    global game_state, score
    ball.center = (WIDTH // 2, HEIGHT // 2)
    ball_speed[0] = BALL_SPEED * random.choice((1, -1))
    ball_speed[1] = BALL_SPEED * random.choice((1, -1))
    game_state = GAME_PLAYING
    score = 0

def move_opponent_paddle(target_y):
    if opponent_paddle.centery < target_y:
        opponent_paddle.centery += ai_speed * ai_skill
    elif opponent_paddle.centery > target_y:
        opponent_paddle.centery -= ai_speed * ai_skill

def increase_ball_speed(difficulty):
    global ai_skill
    if difficulty in difficulty_levels:
        ai_skill = difficulty_levels[difficulty]["ai_skill"]
        ball_speed[0] *= difficulty_levels[difficulty]["ball_speed_multiplier"]
        ball_speed[1] *= difficulty_levels[difficulty]["ball_speed_multiplier"]

def main_menu():
    global game_state, selected_difficulty

    while game_state == MAIN_MENU:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if selected_difficulty:
                        reset_game()
                        increase_ball_speed(selected_difficulty)
                    else:
                        print("Please select a difficulty first.")
                elif event.key == pygame.K_UP:
                    if selected_difficulty == "Extremely Easy":
                        selected_difficulty = "Hacker"
                    elif selected_difficulty:
                        difficulties = list(difficulty_levels.keys())
                        idx = difficulties.index(selected_difficulty)
                        selected_difficulty = difficulties[idx - 1]
                    else:
                        selected_difficulty = "Hacker"
                elif event.key == pygame.K_DOWN:
                    if selected_difficulty == "Hacker":
                        selected_difficulty = "Extremely Easy"
                    elif selected_difficulty:
                        difficulties = list(difficulty_levels.keys())
                        idx = difficulties.index(selected_difficulty)
                        if idx < len(difficulties) - 1:
                            selected_difficulty = difficulties[idx + 1]
                    else:
                        selected_difficulty = "Extremely Easy"

        screen.fill(BLACK)
        font = pygame.font.Font(None, 72)
        title_text = font.render("Pong Game", True, WHITE)
        start_text = font.render("Press ENTER to Start", True, WHITE)
        diff_text = font.render("Difficulty: " + (selected_difficulty or "Select Difficulty"), True, WHITE)
        up_down_text = font.render("Use UP/DOWN arrows to change difficulty", True, WHITE)
        screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, 300))
        screen.blit(start_text, (WIDTH // 2 - start_text.get_width() // 2, 500))
        screen.blit(diff_text, (WIDTH // 2 - diff_text.get_width() // 2, 650))
        screen.blit(up_down_text, (WIDTH // 2 - up_down_text.get_width() // 2, 750))
        pygame.display.flip()

def main_game():
    global game_state, score

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

        move_opponent_paddle(ball.y)

        ball.x += ball_speed[0]
        ball.y += ball_speed[1]

        if ball.colliderect(player_paddle) or ball.colliderect(opponent_paddle):
            ball_speed[0] *= -1

        if ball.top <= 0 or ball.bottom >= HEIGHT:
            ball_speed[1] *= -1

        if ball.left <= 0:
            game_state = GAME_OVER
            score = 0
        elif ball.right >= WIDTH:
            game_state = GAME_OVER
            score = 1

        screen.fill(BLACK)
        pygame.draw.rect(screen, WHITE, player_paddle)
        pygame.draw.rect(screen, WHITE, opponent_paddle)
        pygame.draw.ellipse(screen, WHITE, ball)
        pygame.display.flip()
        pygame.time.Clock().tick(60)

def game_over():
    global game_state

    while game_state == GAME_OVER:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    game_state = MAIN_MENU

        screen.fill(BLACK)
        font = pygame.font.Font(None, 72)
        game_over_text = font.render("Game Over", True, WHITE)
        score_text = font.render("Score: " + ("Win" if score == 1 else "Lose"), True, WHITE)
        restart_text = font.render("Press ENTER to return to the main menu", True, WHITE)
        screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, 300))
        screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, 500))
        screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, 650))
        pygame.display.flip()

if __name__ == "__main__":
    while True:
        if game_state == MAIN_MENU:
            main_menu()
        elif game_state == GAME_PLAYING:
            main_game()
        elif game_state == GAME_OVER:
            game_over()

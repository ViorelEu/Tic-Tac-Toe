import pygame
import sys

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 800
LINE_COLOR = (0, 0, 0)
LINE_WIDTH = 15
CELL_SIZE = WIDTH // 3
BOARD = [[' ' for _ in range(3)] for _ in range(3)]

# Colors
WHITE = (255, 255, 255)
PINK = (255, 51, 148)
BLUE = (0, 0, 255)
current_board_color = PINK
last_color_change_time = 0

# Load X and O images
x_images = [pygame.transform.scale(pygame.image.load(style), (CELL_SIZE, CELL_SIZE)) for style in ["xmagic.png"]]
o_images = [pygame.transform.scale(pygame.image.load(style), (CELL_SIZE, CELL_SIZE)) for style in ["omagic.png"]]
current_x_style = 0
current_o_style = 0

# Initialize the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic-Tac-Toe")

# Function to draw the board
def draw_board():
    pygame.draw.rect(screen, current_board_color, (0, 0, WIDTH, HEIGHT))
    for x in range(1, 3):
        pygame.draw.line(screen, LINE_COLOR, (x * CELL_SIZE, 0), (x * CELL_SIZE, HEIGHT), LINE_WIDTH)
        pygame.draw.line(screen, LINE_COLOR, (0, x * CELL_SIZE), (WIDTH, x * CELL_SIZE), LINE_WIDTH)

# Function to draw X and O
def draw_xo(row, col):
    if BOARD[row][col] == 'X':
        screen.blit(x_images[current_x_style], (col * CELL_SIZE, row * CELL_SIZE))
    elif BOARD[row][col] == 'O':
        screen.blit(o_images[current_o_style], (col * CELL_SIZE, row * CELL_SIZE))

# Function to check for a winner
def check_winner(player):
    for i in range(3):
        if all(BOARD[i][j] == player for j in range(3)) or all(BOARD[j][i] == player for j in range(3)):
            return True
    if all(BOARD[i][i] == player for i in range(3)) or all(BOARD[i][2 - i] == player for i in range(3)):
        return True
    return False

# Function to check for a tie
def check_tie():
    return all(BOARD[i][j] != ' ' for i in range(3) for j in range(3))

# Function to reset the game
def reset_game():
    global BOARD, game_over
    BOARD = [[' ' for _ in range(3)] for _ in range(3)]
    game_over = False

# Function to show a menu
def show_menu():
    # Play background music
    pygame.mixer.music.load("background_music.mp3")
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)  # Play the music in an infinite loop

    menu = True
    while menu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                menu = False

        screen.fill(WHITE)
        font = pygame.font.Font(None, 36)
        menu_text = font.render("Click Anywhere to Start", True, PINK)
        screen.blit(menu_text, (WIDTH // 2 - menu_text.get_width() // 2, HEIGHT // 2 - menu_text.get_height() // 2))
        pygame.display.update()

# Show the initial menu
show_menu()

# Main game loop
turn = 'X'
game_over = False

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if not game_over and event.type == pygame.MOUSEBUTTONDOWN:
            col = event.pos[0] // CELL_SIZE
            row = event.pos[1] // CELL_SIZE
            if BOARD[row][col] == ' ':
                BOARD[row][col] = turn
                if check_winner(turn):
                    game_over = True
                elif check_tie():
                    game_over = True
                turn = 'O' if turn == 'X' else 'X'

        current_time = pygame.time.get_ticks()
        if current_time - last_color_change_time > 2000:
            last_color_change_time = current_time
            current_board_color = BLUE if current_board_color == PINK else PINK

        screen.fill(WHITE)
        draw_board()
        for i in range(3):
            for j in range(3):
                if BOARD[i][j] != ' ':
                    draw_xo(i, j)
        if game_over:
            font = pygame.font.Font(None, 36)
            result_text = font.render("Tie! Click Anywhere for Rematch", True, PINK) if check_tie() else font.render(
                f"{turn} Wins! Click Anywhere for Rematch", True, PINK)
            screen.blit(result_text, (WIDTH // 2 - result_text.get_width() // 2, HEIGHT // 2 - result_text.get_height() // 2))
            wait_for_enter = True
            while wait_for_enter:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        reset_game()
                        show_menu()
                        wait_for_enter = False
        pygame.display.update()

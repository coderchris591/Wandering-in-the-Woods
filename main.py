import pygame
import random
from time import sleep
from config import Config
from menu import main_menu, setup_game

# Initialize Pygame
pygame.init()

# Select mode
mode = main_menu()
config = Config(mode)

# Setup game for modes 3-5 and 6-8
setup_game(config)

# Constants
WIDTH, HEIGHT = 800, 600
GRID_WIDTH, GRID_HEIGHT = config.grid_size

# Calculate cell size to fit the grid on the screen for each player's view
view_width = WIDTH // 2
view_height = HEIGHT // 2

CELL_SIZE = min(view_width // GRID_WIDTH, view_height // GRID_HEIGHT)

# Adjust view width and height to fit the grid perfectly
view_width = GRID_WIDTH * CELL_SIZE
view_height = GRID_HEIGHT * CELL_SIZE

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
PLAYER_COLORS = [GREEN, BLUE, RED, YELLOW]  # Add more colors if needed

# Create screen
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
WIDTH, HEIGHT = screen.get_size()
pygame.display.set_caption("Split-Screen Wandering")

# Load sound and music
win_sound = pygame.mixer.Sound(config.win_sound)
music = pygame.mixer.Sound(config.music)
music.play()
music.set_volume(0.01)

# Load background image
forest_background = pygame.image.load(config.background_image)
forest_background = pygame.transform.scale(forest_background, (view_width, view_height))

def reset_game():
    global mode, config, players, groups, found_each_other, move_count, K2_Step, K2_First_Move, win_time

    # Reset player positions
    # Players (x, y, color)
    players = [
        {"pos": list(pos), "color": PLAYER_COLORS[i], "keys": [pygame.K_w, pygame.K_s, pygame.K_a, pygame.K_d],
         "controls": "WASD"} if i == 0 else
        {"pos": list(pos), "color": PLAYER_COLORS[i],
         "keys": [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT], "controls": "Arrow Keys"} if i == 1 else
        {"pos": list(pos), "color": PLAYER_COLORS[i], "keys": [pygame.K_i, pygame.K_k, pygame.K_j, pygame.K_l],
         "controls": "IJKL"} if i == 2 else
        {"pos": list(pos), "color": PLAYER_COLORS[i], "keys": [pygame.K_t, pygame.K_g, pygame.K_f, pygame.K_h],
         "controls": "TFGH"} for i, pos in enumerate(config.start_positions)
    ]

    # Reset game variables
    groups = [[player] for player in players]
    found_each_other = False
    move_count = 0
    win_time = pygame.time.get_ticks() 
    K2_Step = 0
    K2_First_Move = True # Negates the first move_count since it is not visually represented to the user
    return players, groups, found_each_other, move_count, K2_Step, K2_First_Move, win_time

players, groups, found_each_other, move_count, K2_Step, K2_First_Move, win_time = reset_game()

# Shows results with option to play again and returns updated steps_lowest/steps_highest/average_steps
def results(steps: int,low: int, high: int, average: int, games_played: int, total_steps: int, time: int):
    while True:
        screen.fill(BLACK)
        average = total_steps/games_played
        current_steps = steps
        if steps < low: low = steps
        if steps > high: high = steps 
        text_lines = [
            f"Total steps taken last game: {current_steps}",
            f"Highest steps taken in a game: {high}",
            f"Lowest steps taken in a game: {low}",
            f"Average steps per game: {int(average)}",
            f"Total games played: {games_played}",
        ]
        # Displays time taken to complete only to '6-8' group       
        if mode == '6-8':
            text_lines.append(f"Time played: {round(time/1000,2)} seconds",)           
            text_lines.append("Press 1 to play again or ESC to quit")
        else:
            text_lines.append("Press 1 to play again or ESC to quit")
            
        y_offset = HEIGHT // 2 - 40 
        
        for line in text_lines:
            text = font.render(line, True, BLACK)
            text_rect = text.get_rect(center=(WIDTH // 2, y_offset))
            background_rect = text_rect.inflate(20, 20)
            pygame.draw.rect(screen, WHITE, background_rect)
            screen.blit(text, text_rect)
            y_offset += 60                   

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    return low, high, average, True
                elif event.key == pygame.K_ESCAPE:
                    return low, high, average, False
        pygame.display.flip()
        pygame.time.delay(60)

# Game loop
running = True
font = pygame.font.SysFont(None, 55)
controls_font = pygame.font.SysFont(None, 30)
low_steps = 9999
high_steps = 0 
steps_average = 0 
games_played = 0 
total_steps = 0

while running:
    screen.fill(BLACK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False

    # Get key states
    keys = pygame.key.get_pressed()
    K2_Player = 1

    for group in groups:
        playersInGroup = 1 # Tracks number of players in a group
        if config.random_movement:
            # Random movement for K-2
            dx, dy = random.choice([-1, 1]), random.choice([-1, 1])
            sleep(1)

            for player in group:
                # Starts moving Player 2 towards Player 1
                if K2_Player == 2 and (K2_Step > 10):
                    oldX, oldY = player["pos"][0], player["pos"][1] # Saves current placement of x,y
                    if players[0]["pos"][0] > player["pos"][0]:
                        player["pos"][0] = max(0, min(player["pos"][0] + 1, GRID_WIDTH - 1))
                    elif players[0]["pos"][0] < player["pos"][0]:
                        player["pos"][0] = max(0, min(player["pos"][0] - 1, GRID_WIDTH - 1))
                    if players[0]["pos"][1] > player["pos"][1]:
                        player["pos"][1] = max(0, min(player["pos"][1] + 1, GRID_HEIGHT - 1))
                    elif players[0]["pos"][1] < player["pos"][1]:
                        player["pos"][1] = max(0, min(player["pos"][1] - 1, GRID_HEIGHT - 1))
                    if oldX != player["pos"][0] or oldY != player["pos"][1]: # Compares old placement to new one
                        move_count += 1
                        if K2_First_Move == True:
                            move_count -= 1
                        if playersInGroup > 1: move_count -= 1 # Negates multiples steps from groups that have players > 1
                    playersInGroup += 1
                    K2_Player = 1
                else:
                    oldX, oldY = player["pos"][0], player["pos"][1] # Saves current placement of x,y
                    player["pos"][0] = max(0, min(player["pos"][0] + dx, GRID_WIDTH - 1))
                    player["pos"][1] = max(0, min(player["pos"][1] + dy, GRID_HEIGHT - 1))
                    if oldX != player["pos"][0] or oldY != player["pos"][1]: # Compares old placement to new one
                        move_count += 1
                        if K2_First_Move == True:
                            move_count -= 1
                        if playersInGroup > 1: move_count -= 1 # Negates multiples steps from groups that have players > 1
                    playersInGroup += 1
                    K2_Player = 2
            if K2_Step <= 10: K2_Step += 1
        else:
            # Controlled movement for 3-5 and 6-8
            leader = group[0]
            dx, dy = 0, 0
            if keys[leader["keys"][0]] and leader["pos"][1] > 0:
                dy = -1
            elif keys[leader["keys"][1]] and leader["pos"][1] < GRID_HEIGHT - 1:
                dy = 1
            if keys[leader["keys"][2]] and leader["pos"][0] > 0:
                dx = -1
            elif keys[leader["keys"][3]] and leader["pos"][0] < GRID_WIDTH - 1:
                dx = 1
            for player in group:
                oldX, oldY = player["pos"][0], player["pos"][1] # Saves current placement of x,y
                player["pos"][0] = max(0, min(player["pos"][0] + dx, GRID_WIDTH - 1))
                player["pos"][1] = max(0, min(player["pos"][1] + dy, GRID_HEIGHT - 1))
                if oldX != player["pos"][0] or oldY != player["pos"][1]: # Compares old placement to new one
                    move_count += 1
                    if playersInGroup > 1: move_count -= 1 # Negates multiples steps from groups that have players > 1
                playersInGroup += 1
    K2_First_Move = False


    # Merge groups if they find each other
    new_groups = []
    while groups:
        group = groups.pop(0)
        merged = False
        for other_group in groups:
            if group[0]["pos"] == other_group[0]["pos"]:
                other_group.extend(group)
                merged = True
                break
        if not merged:
            new_groups.append(group)
    groups = new_groups

    # Render split-screen views
    for i, player in enumerate(players):
        view = pygame.Surface((view_width, view_height))
        view.blit(forest_background, (0, 0))
        offset_x = (view_width - GRID_WIDTH * CELL_SIZE) // 2
        offset_y = (view_height - GRID_HEIGHT * CELL_SIZE) // 2
        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                rect = pygame.Rect(x * CELL_SIZE + offset_x, y * CELL_SIZE + offset_y, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(view, BLACK, rect, 1)  # Draw grid lines
                if [x, y] == player["pos"]:
                    group = next(g for g in groups if player in g)
                    if len(group) == 1:
                        pygame.draw.rect(view, player["color"], rect)
                    else:
                        half_width = rect.width // 2
                        half_height = rect.height // 2
                        colors = [p["color"] for p in group]
                        for j, color in enumerate(colors):
                            if j == 0:
                                pygame.draw.rect(view, color, (rect.x, rect.y, half_width, rect.height))
                            elif j == 1:
                                pygame.draw.rect(view, color, (rect.x + half_width, rect.y, half_width, rect.height))
                            elif j == 2:
                                pygame.draw.rect(view, color, (rect.x, rect.y + half_height, rect.width, half_height))
                            elif j == 3:
                                pygame.draw.rect(view, color, (rect.x + half_width, rect.y + half_height, half_width, half_height))
        if config.num_players == 3:
            if i == 0:
                screen.blit(view, ((WIDTH // 2 - view_width) // 2, (HEIGHT // 2 - view_height) // 2))
                controls_text = controls_font.render("Controls: WASD", True, WHITE)
                screen.blit(controls_text, ((WIDTH // 2 - view_width) // 2, (HEIGHT // 2 - view_height) // 2 + view_height + 10))
            elif i == 1:
                screen.blit(view, ((WIDTH // 2 - view_width) // 2 + WIDTH // 2, (HEIGHT // 2 - view_height) // 2))
                controls_text = controls_font.render("Controls: Arrow Keys", True, WHITE)
                screen.blit(controls_text, ((WIDTH // 2 - view_width) // 2 + WIDTH // 2, (HEIGHT // 2 - view_height) // 2 + view_height + 10))
            elif i == 2:
                screen.blit(view, ((WIDTH // 2 - view_width) // 2, (HEIGHT // 2 - view_height) // 2 + HEIGHT // 2))
                controls_text = controls_font.render("Controls: IJKL", True, WHITE)
                screen.blit(controls_text, ((WIDTH // 2 - view_width) // 2, (HEIGHT // 2 - view_height) // 2 + HEIGHT // 2 + view_height + 10))
        else:
            row = i // 2
            col = i % 2
            screen.blit(view, (col * WIDTH // 2 + (WIDTH // 2 - view_width) // 2, row * HEIGHT // 2 + (HEIGHT // 2 - view_height) // 2))
            controls_text = controls_font.render(f"Controls: {player['controls']}", True, WHITE)
            screen.blit(controls_text, (col * WIDTH // 2 + (WIDTH // 2 - view_width) // 2, row * HEIGHT // 2 + (HEIGHT // 2 - view_height) // 2 + view_height + 10))

    # Draw dividing lines
    pygame.draw.line(screen, BLACK, (WIDTH // 2, 0), (WIDTH // 2, HEIGHT), 2)
    pygame.draw.line(screen, BLACK, (0, HEIGHT // 2), (WIDTH, HEIGHT // 2), 2)

    # Check if all players found each other
    if len(groups) == 1 and len(groups[0]) == config.num_players:
        if not found_each_other:
            win_sound.play()
            found_each_other = True
            win_time = pygame.time.get_ticks() - win_time
           
        text_string = (f"You found each other! Move Count: {move_count}")
        text = font.render(text_string, True, BLACK)
        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        background_rect = text_rect.inflate(20, 20)
        pygame.draw.rect(screen, WHITE, background_rect)
        screen.blit(text, text_rect)
        pygame.display.flip()
        pygame.time.delay(3000)
        
        games_played += 1
        total_steps += move_count
        low_steps, high_steps, steps_average, running = results(move_count,low_steps, high_steps, steps_average, games_played, total_steps, win_time)
        
        reset_game()  # Reset game
        found_each_other = False  # Reset game state

    pygame.display.flip()
    pygame.time.delay(100)

pygame.quit()




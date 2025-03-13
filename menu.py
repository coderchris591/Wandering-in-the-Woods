import pygame

def draw_text(screen, text, font, color, center):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=center)
    screen.blit(text_surface, text_rect)

def main_menu():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Select Game Mode")
    font = pygame.font.SysFont(None, 55)
    small_font = pygame.font.SysFont(None, 35)
    clock = pygame.time.Clock()
    selected_mode = None
    

    # Load background image
    background_image = pygame.image.load('menu_background.jpg')
    background_image = pygame.transform.scale(background_image, (800, 600))

    while selected_mode is None:
        screen.blit(background_image, (0, 0))
        draw_text(screen, "Select Game Mode", font, (255, 255, 255), (400, 100))
        draw_text(screen, "1. K-2", small_font, (255, 255, 255), (400, 250))
        draw_text(screen, "2. 3-5", small_font, (255, 255, 255), (400, 350))
        draw_text(screen, "3. 6-8", small_font, (255, 255, 255), (400, 450))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    selected_mode = 'K-2'
                elif event.key == pygame.K_2:
                    selected_mode = '3-5'
                elif event.key == pygame.K_3:
                    selected_mode = '6-8'

        pygame.display.flip()
        clock.tick(60)

    return selected_mode

def setup_game(config):
    if config.mode == 'K-2':
        return

    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Setup Game")
    font = pygame.font.SysFont(None, 55)
    small_font = pygame.font.SysFont(None, 35)
    clock = pygame.time.Clock()
    input_active = False
    input_text = ""
    step = 0
    error_message = ""

    # Load background image
    background_image = pygame.image.load('menu_background.jpg')
    background_image = pygame.transform.scale(background_image, (800, 600))

    while True:
        screen.blit(background_image, (0, 0))
        if step == 0:
            draw_text(screen, "Enter Grid Width:", font, (255, 255, 255), (400, 100))
        elif step == 1:
            draw_text(screen, "Enter Grid Height:", font, (255, 255, 255), (400, 100))
        elif step == 2:
            draw_text(screen, "Enter Number of Players (2-4):", font, (255, 255, 255), (400, 100))
        elif step >= 3:
            draw_text(screen, f"Enter Start Position for Player {step - 2} (x,y):", font, (255, 255, 255), (400, 100))

        draw_text(screen, input_text, small_font, (255, 255, 255), (400, 300))
        if error_message:
            draw_text(screen, error_message, small_font, (255, 0, 0), (400, 350))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if input_text.strip():
                        try:
                            if step == 0:
                                config.set_grid_size(int(input_text), config.grid_size[1])
                            elif step == 1:
                                config.set_grid_size(config.grid_size[0], int(input_text))
                            elif step == 2:
                                num_players = int(input_text)
                                if num_players < 2 or num_players > 4:
                                    raise ValueError("Number of players must be between 2 and 4.")
                                config.set_num_players(num_players)
                                config.start_positions = [(0, 0)] * config.num_players  # Initialize start positions
                            else:
                                x, y = map(int, input_text.split(','))
                                if step - 3 < config.num_players:
                                    config.start_positions[step - 3] = (x, y)
                                else:
                                    raise ValueError("Too many start positions entered.")

                            input_text = ""
                            error_message = ""
                            step += 1
                            if step >= 3 + config.num_players:
                                return
                        except ValueError as e:
                            error_message = f"Invalid input: {e}"
                            input_text = ""
                elif event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                else:
                    input_text += event.unicode

        pygame.display.flip()
        clock.tick(60)

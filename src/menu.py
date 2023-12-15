import pygame


class Menu:
    """
    Represents the main menu in the game.
    """
    def __init__(self):
        # Load image for menu.
        self.image = pygame.transform.scale(pygame.image.load("assets/images/menu.png").convert_alpha(), (1344, 768))
        self.font_big = pygame.font.Font("assets/fonts/stacker.ttf", 100)
        self.font_small = pygame.font.Font("assets/fonts/stacker.ttf", 60)
        self.settings_icon = pygame.transform.scale_by(
            pygame.image.load("assets/images/settings.png").convert_alpha(), 0.3)
        self.quit_icon = pygame.transform.scale_by(
            pygame.image.load("assets/images/quit.png").convert_alpha(), 0.15)
        self.play_button = None
        self.settings_button = None
        self.stats_button = None
        self.shop_button = None
        self.quit_button = None

    def display(self, screen):
        """
        Displays the menu on the screen.
        """
        # Draw background image on screen.
        screen.blit(self.image, (0, 0))

        # Draw play button on screen.
        self.play_button = draw_button(screen, self.image.get_rect().center, (255, 0, 255), "PLAY",
                                       (0, 255, 255), self.font_big)

        # Draw settings button on screen.
        self.settings_button = draw_button(screen, (self.image.get_rect().centerx, 65), border_color=(0, 0, 255),
                                           text_color=(0, 255, 255), image=self.settings_icon)

        # Draw statistics button on screen.
        self.stats_button = draw_button(screen, (self.play_button.left / 2 - 50, self.play_button.centery),
                                        (0, 255, 255), "STATS", (0, 150, 255), self.font_small)

        # Draw shop button on screen.
        self.shop_button = draw_button(screen, (self.image.get_width() - self.stats_button.centerx,
                                                self.play_button.centery), (0, 255, 255), "SHOP",
                                       (0, 150, 255), self.font_small)

        # Draw quit button on screen.
        self.quit_button = draw_button(screen, (self.image.get_rect().centerx, self.image.get_height() - 65),
                                       (0, 0, 255), image=self.quit_icon)

        # Update display.
        pygame.display.flip()

    def handle_input(self):
        """
        Handles user input for the menu.
        """
        # Check for mouse clicks.
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if pygame.mouse.get_pressed()[0]:
            if self.play_button.collidepoint(mouse_x, mouse_y):
                return "play"
            elif self.settings_button.collidepoint(mouse_x, mouse_y):
                return "settings"
            elif self.stats_button.collidepoint(mouse_x, mouse_y):
                return "stats"
            elif self.quit_button.collidepoint(mouse_x, mouse_y):
                return "quit"
            elif self.shop_button.collidepoint(mouse_x, mouse_y):
                return "shop"

        # Update display.
        pygame.display.flip()


class GameOverMenu:
    """
    Represents the game over screen.
    """
    def __init__(self):
        # Load game over image.
        self.image = pygame.transform.scale_by(pygame.image.load("assets/images/game_over.png").convert_alpha(), 0.5)

    def show(self, screen, distance, highscore):
        # Fill background with black.
        screen.fill((0, 0, 0))

        # Draw game over image on screen.
        screen.blit(self.image, ((screen.get_width() - self.image.get_width()) / 2,
                                 (screen.get_height() - self.image.get_height()) / 2))
        # Font for texts.
        font = pygame.font.SysFont("comicsansms", 72)

        # Text for travelled score.
        score_surface = font.render(f"Reached Score: {distance}", True, (0, 0, 255))
        screen.blit(score_surface, ((screen.get_width() - score_surface.get_width()) / 2, 80))

        # Text for highscore.
        highscore_surface = font.render(f"Highscore: {highscore}", True, (0, 0, 255))
        screen.blit(highscore_surface, ((screen.get_width() - highscore_surface.get_width()) / 2, 180))

        # Text for restarting game.
        text_surface = font.render("Press space to run!", True, (0, 0, 255))
        screen.blit(text_surface, ((screen.get_width() - text_surface.get_width()) / 2, 500))

        # Update display.
        pygame.display.flip()


class PauseMenu:
    """
    Represents the pause screen.
    """
    def __init__(self):
        # Load background image for pause screen.
        self.image = pygame.transform.scale_by(pygame.image.load("assets/images/pause.png").convert_alpha(), 0.15)
        self.rect = self.image.get_rect()

        # Font for texts.
        self.font_large = pygame.font.SysFont("comicsansms", 65)
        self.font_small = pygame.font.SysFont("comicsansms", 50)

    def handle_input(self, screen):
        """
        Handles user input for the pause menu.

        Returns:
            str: The action based on the button clicked ('resume', 'main_menu', 'quit').
        """
        # Draw background image on screen.
        self.rect.topleft = ((screen.get_width() - self.image.get_width()) / 2, (screen.get_height() - self.image.get_height()) / 2)
        screen.blit(self.image, self.rect.topleft)

        # Paused text.
        paused = self.font_large.render("PAUSED", True, (0, 255, 255))
        screen.blit(paused, (self.rect.centerx - paused.get_width() / 2, self.rect.top))

        # Button for resuming game.
        resume_button_rect = draw_button(screen, (self.rect.centerx, 275), (0, 255, 0), "RESUME", (0, 255, 0),
                                         self.font_small)

        # Button for returning to the main menu.
        main_menu_button_rect = draw_button(screen, (self.rect.centerx, 375), (0, 0, 255), "MAIN MENU", (0, 0, 255),
                                            self.font_small)

        # Button for quitting the game.
        quit_button_rect = draw_button(screen, (self.rect.centerx, 475), (255, 0, 0), "QUIT", (255, 0, 0),
                                       self.font_small)

        # Check for mouse clicks.
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if pygame.mouse.get_pressed()[0]:
            if resume_button_rect.collidepoint(mouse_x, mouse_y):
                return "resume"
            elif main_menu_button_rect.collidepoint(mouse_x, mouse_y):
                return "main_menu"
            elif quit_button_rect.collidepoint(mouse_x, mouse_y):
                return "quit"

        # Update display.
        pygame.display.flip()


def draw_button(screen, position, border_color, text=None, text_color=None, font=None, image=None):
    """
    Draw a button on the screen.

    Args:
        screen (pygame.Surface): The screen to draw on.
        position (tuple): The position of the button's center.
        border_color (tuple): The color of the border.
        text_color (tuple): The color of the button.
        text (str): The text to display on the button.
        font (pygame.font.Font): The font for the button text.
        image (pygame.image): The image of the button.

    Returns:
        pygame.Rect: The rectangle representing the button's position and size.
    """
    if text and text_color and font:
        button = font.render(text, True, text_color)
    else:
        button = image
    button_rect = button.get_rect(center=position)
    pygame.draw.rect(screen, border_color, button_rect.inflate(30, 10), 5, border_radius=25)
    screen.blit(button, (button_rect.x, button_rect.y))
    return button_rect

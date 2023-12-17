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
        self.clicked_play_button = False
        self.settings_button = None
        self.clicked_settings_button = False
        self.stats_button = None
        self.clicked_stats_button = False
        self.shop_button = None
        self.clicked_shop_button = False
        self.quit_button = None
        self.clicked_quit_button = False

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

    def handle_input(self, event):
        """
        Handles user input for the menu.
        """
        # Check for mouse clicks.
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.play_button.collidepoint(mouse_x, mouse_y):
                self.clicked_play_button = True
            elif self.settings_button.collidepoint(mouse_x, mouse_y):
                self.clicked_settings_button = True
            elif self.stats_button.collidepoint(mouse_x, mouse_y):
                self.clicked_stats_button = True
            elif self.quit_button.collidepoint(mouse_x, mouse_y):
                self.clicked_quit_button = True
            elif self.shop_button.collidepoint(mouse_x, mouse_y):
                self.clicked_shop_button = True
        elif event.type == pygame.MOUSEBUTTONUP:
            if self.play_button.collidepoint(mouse_x, mouse_y) and self.clicked_play_button:
                self.clicked_play_button = False
                return "play"
            elif self.settings_button.collidepoint(mouse_x, mouse_y) and self.clicked_settings_button:
                self.clicked_settings_button = False
                return "settings"
            elif self.stats_button.collidepoint(mouse_x, mouse_y) and self.clicked_stats_button:
                self.clicked_stats_button = False
                return "stats"
            elif self.quit_button.collidepoint(mouse_x, mouse_y) and self.clicked_quit_button:
                self.clicked_quit_button = False
                return "quit"
            elif self.shop_button.collidepoint(mouse_x, mouse_y) and self.clicked_shop_button:
                self.clicked_shop_button = False
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

        self.resume_button = None
        self.clicked_resume = False
        self.main_menu_button = None
        self.clicked_main_menu = False
        self.quit_button = None
        self.clicked_quit = False

    def display(self, screen):
        # Draw background image on screen.
        self.rect.topleft = ((screen.get_width() - self.image.get_width()) / 2, (
                screen.get_height() - self.image.get_height()) / 2)
        screen.blit(self.image, self.rect.topleft)

        # Paused text.
        paused = self.font_large.render("PAUSED", True, (0, 255, 255))
        screen.blit(paused, (self.rect.centerx - paused.get_width() / 2, self.rect.top))

        # Button for resuming game.
        self.resume_button = draw_button(screen, (self.rect.centerx, 275), (0, 255, 0), "RESUME", (0, 255, 0),
                                         self.font_small)

        # Button for returning to the main menu.
        self.main_menu_button = draw_button(screen, (self.rect.centerx, 375), (0, 0, 255), "MAIN MENU", (0, 0, 255),
                                            self.font_small)

        # Button for quitting the game.
        self.quit_button = draw_button(screen, (self.rect.centerx, 475), (255, 0, 0), "QUIT", (255, 0, 0),
                                       self.font_small)

        # Update display.
        pygame.display.flip()

    def handle_input(self, event):
        """
        Handles user input for the pause menu.

        Returns:
            str: The action based on the button clicked ('resume', 'main_menu', 'quit').
        """
        # Check for mouse clicks.
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.resume_button.collidepoint(mouse_x, mouse_y):
                self.clicked_resume = True
            elif self.main_menu_button.collidepoint(mouse_x, mouse_y):
                self.clicked_main_menu = True
            elif self.quit_button.collidepoint(mouse_x, mouse_y):
                self.clicked_quit = True
        elif event.type == pygame.MOUSEBUTTONUP:
            if self.resume_button.collidepoint(mouse_x, mouse_y) and self.clicked_resume:
                self.clicked_resume = False
                return "resume"
            elif self.main_menu_button.collidepoint(mouse_x, mouse_y) and self.clicked_main_menu:
                self.clicked_main_menu = False
                return "main_menu"
            elif self.quit_button.collidepoint(mouse_x, mouse_y) and self.clicked_quit:
                self.clicked_quit = False
                return "quit"


class SettingsMenu:
    """
    Represents the settings menu.
    """
    def __init__(self, game):
        self.image = pygame.transform.scale(pygame.image.load("assets/images/menu.png").convert_alpha(), (1344, 768))
        self.settings_icon = pygame.transform.scale_by(
            pygame.image.load("assets/images/settings.png").convert_alpha(), 0.5)
        self.font_big = pygame.font.Font("assets/fonts/stacker.ttf", 60)
        self.font_small = pygame.font.Font("assets/fonts/stacker.ttf", 30)
        self.number_font = pygame.font.SysFont("comicsans", 30)
        self.sliders = {
            "music_slider":
                Slider((self.image.get_rect().centerx / 2 - 125, self.image.get_rect().centery + 30), (200, 40),
                       0.5, 0, 100, self.number_font),
            "sound_slider":
                Slider((self.image.get_rect().centerx + 450, self.image.get_rect().centery + 30),
                       (200, 40), 0.5, 0, 100, self.number_font)}
        self.game = game

    def display(self, screen):
        # Draw background image on screen.
        screen.blit(self.image, (0, 0))

        # Draw settings button on screen.
        draw_button(screen, self.image.get_rect().center, border_color=(0, 0, 255),
                    text_color=(0, 255, 255), image=self.settings_icon)

        # Texts for music and sound volume.
        music_volume = self.font_small.render("Music Volume", True, (0, 255, 255))
        screen.blit(music_volume, (self.image.get_rect().centerx / 2 - 250, self.image.get_rect().centery - 70))
        sound_volume = self.font_small.render("Sound Volume", True, (0, 255, 255))
        screen.blit(sound_volume, (self.image.get_rect().centerx + 315, self.image.get_rect().centery - 70))

        # Draw back button on screen.
        back_button = draw_button(screen, (self.image.get_rect().centerx, self.image.get_height() - 80),
                                  border_color=(0, 255, 255), text="BACK", text_color=(0, 150, 255), font=self.font_big)

        self.handle_input(screen)

        # Update display.
        pygame.display.flip()

    def handle_input(self, screen):
        mouse_pos = pygame.mouse.get_pos()
        mouse = pygame.mouse.get_pressed()

        for name, slider in self.sliders.items():
            if slider.container_rect.collidepoint(mouse_pos):
                if mouse[0]:
                    slider.grabbed = True
            if not mouse[0]:
                slider.grabbed = False
            if slider.button_rect.collidepoint(mouse_pos):
                slider.hover()
            if slider.grabbed:
                slider.move_slider(mouse_pos)
                slider.hover()
            else:
                slider.hovered = False
            slider.render(screen)
            slider.display_value(screen)
            if name == "music_slider":
                self.game.music.set_volume(int(slider.get_value() / 100))
            elif name == "sound_slider":
                [sound.set_volume(int(slider.get_value() / 100)) for sound in self.game.sounds.values()]


class Slider:
    def __init__(self, pos, size, initial_val, min, max, font):
        self.pos = pos
        self.size = size
        self.font = font
        self.hovered = False
        self.grabbed = False
        self.unselected_color = "blue"
        self.selected_color = "white"
        self.button_states = {
            True: self.selected_color,
            False: self.unselected_color
        }

        self.slider_left_pos = self.pos[0] - (size[0] // 2)
        self.slider_right_pos = self.pos[0] + (size[0] // 2)
        self.slider_top_pos = self.pos[1] - (size[1] // 2)

        self.min = min
        self.max = max
        self.initial_val = (self.slider_right_pos - self.slider_left_pos) * initial_val  # <- percentage

        self.container_rect = pygame.Rect(self.slider_left_pos, self.slider_top_pos, self.size[0], self.size[1])
        self.button_rect = pygame.Rect(self.slider_left_pos + self.initial_val - 5, self.slider_top_pos, 10,
                                       self.size[1])

        # label
        self.text = self.font.render(str(int(self.get_value())), True, "white")
        self.label_rect = self.text.get_rect(center=(self.pos[0], self.slider_top_pos - 15))

    def move_slider(self, mouse_pos):
        pos = mouse_pos[0]
        if pos < self.slider_left_pos:
            pos = self.slider_left_pos
        if pos > self.slider_right_pos:
            pos = self.slider_right_pos
        self.button_rect.centerx = pos

    def hover(self):
        self.hovered = True

    def render(self, screen):
        pygame.draw.rect(screen, "darkgray", self.container_rect)
        pygame.draw.rect(screen, self.button_states[self.hovered], self.button_rect)

    def get_value(self):
        val_range = self.slider_right_pos - self.slider_left_pos - 1
        button_val = self.button_rect.centerx - self.slider_left_pos

        return (button_val / val_range) * (self.max - self.min) + self.min

    def display_value(self, screen):
        self.text = self.font.render(str(int(self.get_value())), True, "white")
        screen.blit(self.text, self.label_rect)


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

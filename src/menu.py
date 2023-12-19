import pygame
import pandas as pd
import numpy as np


class Menu:
    """
    Base class for menus with 5 areas (center, top, bottom, left, right).
    """

    def __init__(self, game):
        self.image = pygame.transform.scale(pygame.image.load("assets/images/menu.png").convert_alpha(), (1344, 768))
        self.image_rect = self.image.get_rect()
        self.font_big = pygame.font.Font("assets/fonts/stacker.ttf", 100)
        self.font_middle = pygame.font.Font("assets/fonts/stacker.ttf", 60)
        self.font_small = pygame.font.Font("assets/fonts/stacker.ttf", 30)
        self.font_comicsans = pygame.font.SysFont("comicsans", 30)
        self.font_comicsans_small = pygame.font.SysFont("comicsans", 22)
        self.game = game
        self.center = self.image_rect.center
        self.top = (self.center[0], 65)
        self.bottom = (self.center[0], self.image_rect.height - 65)
        self.left = (self.center[0] // 2, self.center[1])
        self.right = (self.center[0] + self.center[0] // 2, self.center[1])
        self.settings_icon_big = pygame.transform.scale_by(
            pygame.image.load("assets/images/settings.png").convert_alpha(), 0.6)
        self.settings_icon_small = pygame.transform.scale_by(self.settings_icon_big, 0.5)
        self.quit_icon = pygame.transform.scale_by(
            pygame.image.load("assets/images/quit.png").convert_alpha(), 0.15)
        self.stats_icon = pygame.transform.scale_by(pygame.image.load("assets/images/statistics.png").convert_alpha(),
                                                    0.2)
        self.shop_icon = pygame.transform.scale_by(pygame.image.load("assets/images/shopping_cart.png").convert_alpha(),
                                                   0.05)
        self.heart_icon = pygame.transform.scale_by(pygame.image.load("assets/images/heart.png").convert_alpha(),
                                                    0.03)
        self.weapon_icon = pygame.transform.scale_by(
            pygame.image.load("assets/images/player/weapon/weapon2_right.png").convert_alpha(), 5)
        self.buttons = []
        self.sliders = []

    def display(self, pos=None):
        """
        Displays menu on the screen.
        """
        # Draw background image on the screen.
        if pos:
            topleft = ((self.game.screen.get_width() - self.image.get_width()) / 2, (
                    self.game.screen.get_height() - self.image.get_height()) / 2)
            self.game.screen.blit(self.image, topleft)
        else:
            self.game.screen.blit(self.image, (0, 0))

        # Draw buttons on the screen.
        for button in self.buttons:
            button.render()

        # Draw sliders on the screen.
        for slider in self.sliders:
            slider.render()
            slider.display_value()

    def handle_input(self, event):
        """
        Handles user input for the menu.

        Returns:
            Name of the clicked button if a button was clicked.
        """
        # Get mouse position and clicked mouse buttons.
        mouse_pos = pygame.mouse.get_pos()
        mouse = pygame.mouse.get_pressed()

        # Handle sliders.
        for slider in self.sliders:
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
            slider.render()
            slider.display_value()

        # Check whether mouse position collides with buttons.
        cursor_over_button = any(
            button.rect.collidepoint(mouse_pos) and "text" not in button.name and "icon" not in button.name for button
            in self.buttons)

        # Set cursor based on collision with button.
        if cursor_over_button:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

        # Handle mouse clicks for buttons.
        if event.type == pygame.MOUSEBUTTONDOWN:
            for button in self.buttons:
                if button.rect.collidepoint(mouse_pos):
                    button.clicked = True
        elif event.type == pygame.MOUSEBUTTONUP:
            for button in self.buttons:
                if button.rect.collidepoint(mouse_pos) and button.clicked:
                    button.clicked = False
                    return button.name


class MainMenu(Menu):
    """
    Represents the main menu in the game.
    """

    def __init__(self, game):
        super().__init__(game)
        self.buttons = [
            Button("play_button", self.game.screen, self.center, "magenta", "play", "cyan", self.font_big),
            Button("settings_button", self.game.screen, self.top, "blue", None, None, None, self.settings_icon_small),
            Button("stats_button", self.game.screen, self.left, "cyan", "stats", "dodgerblue", self.font_middle),
            Button("shop_button", self.game.screen, self.right, "cyan", "shop", "dodgerblue", self.font_middle),
            Button("quit_button", self.game.screen, self.bottom, "blue", None, None, None, self.quit_icon)
        ]

    def display(self):
        """
        Displays the menu on the screen.
        """
        super().display()

        # Update display.
        pygame.display.flip()

    def handle_input(self, event):
        """
        Handles user input for the menu.
        """
        clicked_button = super().handle_input(event)
        return clicked_button


class SettingsMenu(Menu):
    """
    Represents the settings menu.
    """

    def __init__(self, game):
        super().__init__(game)

        self.sliders = [
            Slider("music_slider", self.game.screen,
                   self.left, (200, 40), self.game.music.get_volume(), 0, 100, self.font_comicsans),
            Slider("volume_slider", self.game.screen,
                   self.right, (200, 40), self.game.sounds['shoot'].get_volume(), 0, 100, self.font_comicsans)
        ]
        self.buttons = [
            Button("settings_text", self.game.screen, (self.top[0], self.top[1] + 15), "cyan", "settings",
                   "dodgerblue", self.font_middle),
            Button("settings_icon", self.game.screen, self.center, "blue", None, None, None, self.settings_icon_big),
            Button("back_button", self.game.screen, self.bottom, "cyan", "back", "dodgerblue", self.font_middle)
        ]

    def display(self):
        super().display()

        # Texts for music and sound volume.
        music_volume = self.font_small.render("Music Volume", True, (0, 255, 255))
        music_volume_rect = music_volume.get_rect(center=(self.left[0] - 100, self.left[1] - 50))
        self.game.screen.blit(music_volume, music_volume_rect)
        sound_volume = self.font_small.render("Sound Volume", True, (0, 255, 255))
        sound_volume_rect = sound_volume.get_rect(center=(self.right[0] + 100, self.right[1] - 50))
        self.game.screen.blit(sound_volume, sound_volume_rect)

        # Update display.
        pygame.display.flip()

    def handle_input(self, event):
        for slider in self.sliders:
            if slider.name == "music_slider":
                self.game.music.set_volume(round(slider.get_value() / 100, 2))
            elif slider.name == "volume_slider":
                [sound.set_volume(round(slider.get_value() / 100, 2)) for sound in self.game.sounds.values()]

        clicked_button = super().handle_input(event)
        return clicked_button


class StatsMenu(Menu):
    """
    Represents the statistcs menu.
    """

    def __init__(self, game):
        super().__init__(game)

        self.buttons = [
            Button("stats_text", self.game.screen, (self.top[0], self.top[1] + 15), "cyan", "statistics",
                   "dodgerblue", self.font_middle),
            Button("stats_icon", self.game.screen, self.center, "blue", None, None, None, self.stats_icon),
            Button("back_button", self.game.screen, self.bottom, "cyan", "back", "dodgerblue", self.font_middle)
        ]

    def display(self):
        super().display()

        # Get highscore and travelled distance of last 10 runs .
        highscore, run_distance_df, distance_list = self.get_highscore_and_run_distance()

        # Display dataframe with travelled distance of last 10 runs as table.
        self.display_table(run_distance_df)

        # Display highscore.
        highscore_text = self.font_small.render("Highscore", True, "cyan")
        highscore_text_rect = highscore_text.get_rect(center=(self.right[0] + 100, self.right[1] - 70))
        highscore_number = self.font_comicsans.render(str(highscore), True, "dodgerblue")
        highscore_number_rect = highscore_number.get_rect(center=(self.right[0] + 100, self.right[1] - 35))
        self.game.screen.blit(highscore_text, highscore_text_rect)
        self.game.screen.blit(highscore_number, highscore_number_rect)

        # Display average distance.
        average_text = self.font_small.render("Average Distance", True, "cyan")
        average_text_rect = average_text.get_rect(center=(self.right[0] + 100, self.right[1] + 35))
        average_number = self.font_comicsans.render(str(int(np.mean(distance_list))), True, "dodgerblue")
        average_number_rect = average_number.get_rect(center=(self.right[0] + 100, self.right[1] + 70))
        self.game.screen.blit(average_text, average_text_rect)
        self.game.screen.blit(average_number, average_number_rect)

        # Update display.
        pygame.display.flip()

    def get_highscore_and_run_distance(self):
        # Get highscore and distance of last 10 runs.
        highscore, run_distance_list = self.game.save_load_manager.load_game_data(["highscore", "run_distance"],
                                                                                  [0, [0, 0]])
        run_list = []
        distance_list = []
        for index, run_distance in enumerate(run_distance_list[-22:]):
            if index > 1:
                if (index + 1) % 2 == 0:
                    distance_list.append(run_distance)
                else:
                    run_list.append(run_distance)

        # Create DataFrame from distance and run lists for table format.
        run_distance_dict = {"Run": run_list, "Distance": distance_list}
        run_distance_df = pd.DataFrame(run_distance_dict)

        return highscore, run_distance_df, distance_list

    def display_table(self, table_df):
        # Cell and table settings
        cell_padding = 5
        table_x, table_y = self.left[0] - 250, self.left[1] - 250
        cell_width = 150
        cell_height = 40

        # Draw the table columns.
        for i, col in enumerate(table_df.columns):
            cell_rect = pygame.Rect(table_x + i * cell_width, table_y, cell_width, cell_height)
            pygame.draw.rect(self.game.screen, (50, 50, 50), cell_rect)
            cell_text = self.font_comicsans_small.render(col, True, "cyan")
            self.game.screen.blit(cell_text, (cell_rect.x + cell_padding, cell_rect.y + cell_padding))

        # Draw the table rows.
        for i, (_, row) in enumerate(table_df.iterrows()):
            for j, value in enumerate(row):
                cell_rect = pygame.Rect(table_x + j * cell_width, table_y + (i + 1) * cell_height, cell_width,
                                        cell_height)
                pygame.draw.rect(self.game.screen, (100, 100, 100) if i % 2 == 0 else (80, 80, 80), cell_rect)
                cell_text = self.font_comicsans_small.render(str(value), True, "cyan")
                self.game.screen.blit(cell_text, (cell_rect.x + cell_padding, cell_rect.y + cell_padding))

    def handle_input(self, event):
        clicked_button = super().handle_input(event)
        return clicked_button


class ShopMenu(Menu):
    """
    Represents the shop menu.
    """

    def __init__(self, game):
        super().__init__(game)

        self.buttons = [
            Button("shop_text", self.game.screen, (self.top[0], self.top[1] + 15), "cyan", "shop",
                   "dodgerblue", self.font_middle),
            Button("shop_icon", self.game.screen, self.center, "blue", None, None, None, self.shop_icon),
            Button("heart_icon", self.game.screen, (self.left[0] - 100, self.left[1] - 40), "red",
                   None, None, None, self.heart_icon),
            Button("buy_second_life_button", self.game.screen, (self.left[0] - 100, self.left[1] + 50), "dodgerblue",
                   "buy", "cyan", self.font_small),
            Button("weapon_icon", self.game.screen, (self.right[0] + 100, self.right[1] - 40), "grey",
                   None, None, None, self.weapon_icon),
            Button("buy_weapon_button", self.game.screen, (self.right[0] + 100, self.right[1] + 50), "dodgerblue",
                   "buy", "cyan", self.font_small),
            Button("back_button", self.game.screen, self.bottom, "cyan", "back", "dodgerblue", self.font_middle)
        ]

    def display(self):
        super().display()

        # Update display.
        pygame.display.flip()

    def handle_input(self, event):
        clicked_button = super().handle_input(event)
        return clicked_button


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


class PauseMenu(Menu):
    """
    Represents the pause screen.
    """

    def __init__(self, game):
        super().__init__(game)

        # Load different background image for pause screen.
        self.image = pygame.transform.scale_by(pygame.image.load("assets/images/pause.png").convert_alpha(), 0.15)

        self.buttons = [
            Button("resume_button", self.game.screen, (self.image_rect.centerx, 275), "green", "resume", "green",
                   self.font_small),
            Button("main_menu_button", self.game.screen, (self.image_rect.centerx, 375), "dodgerblue", "main menu",
                   "dodgerblue", self.font_small),
            Button("quit_button", self.game.screen, (self.image_rect.centerx, 475), "red", "quit", "red",
                   self.font_small)
        ]

    def display(self):
        pos = (self.game.screen.get_width() - self.image_rect.width // 2,
               self.game.screen.get_height() - self.image_rect.width // 2)
        super().display(pos)

        # Paused text.
        paused = self.font_middle.render("paused", True, "cyan")
        self.game.screen.blit(paused, (self.image_rect.centerx - paused.get_width() // 2, 100))

        # Update display.
        pygame.display.flip()

    def handle_input(self, event):
        """
        Handles user input for the pause menu.

        Returns:
            str: The action based on the button clicked ('resume', 'main_menu', 'quit').
        """
        clicked_button = super().handle_input(event)
        return clicked_button


class Slider:
    def __init__(self, name, screen, pos, size, initial_val, min, max, font):
        self.name = name
        self.screen = screen
        self.size = size
        if name == "music_slider":
            self.pos = (pos[0] - self.size[0] // 2, pos[1] + 30)
        elif name == "volume_slider":
            self.pos = (pos[0] + self.size[0] // 2, pos[1] + 30)
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
        self.initial_val = (self.slider_right_pos - self.slider_left_pos) * initial_val

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

    def render(self):
        pygame.draw.rect(self.screen, "darkgray", self.container_rect)
        pygame.draw.rect(self.screen, self.button_states[self.hovered], self.button_rect)

    def get_value(self):
        val_range = self.slider_right_pos - self.slider_left_pos - 1
        button_val = self.button_rect.centerx - self.slider_left_pos

        return (button_val / val_range) * (self.max - self.min) + self.min

    def display_value(self):
        self.text = self.font.render(str(int(self.get_value())), True, "white")
        self.screen.blit(self.text, self.label_rect)


class Button:
    """
    Represents a button.
    """

    def __init__(self, name, screen, position, border_color, text, text_color, font, image=None):
        self.name = name
        self.screen = screen
        self.position = position
        self.border_color = border_color
        self.text = text
        self.text_color = text_color
        self.font = font
        self.image = image
        self.rect = None
        self.clicked = False

    def render(self):
        """
        Renders button to the screen.
        """
        # Check whether button has an image or text.
        if self.image:
            button = self.image
        else:
            button = self.font.render(self.text, True, self.text_color)

        # Update left or right button position based on button width.
        if self.position[0] == self.screen.get_width() // 4:
            self.position = (self.position[0] - button.get_rect().width // 2, self.position[1])
        elif self.position[0] == self.screen.get_width() - self.screen.get_width() // 4:
            self.position = (self.position[0] + button.get_rect().width // 2, self.position[1])

        self.rect = button.get_rect(center=self.position)
        pygame.draw.rect(self.screen, self.border_color, self.rect.inflate(30, 10), 5, border_radius=25)
        self.screen.blit(button, (self.rect.x, self.rect.y))

import pygame
import pandas as pd
import numpy as np
from src.assets import Assets


class Menu:
    """
    Base class for menus with 5 areas (center, top, bottom, left, right).
    """

    def __init__(self, game):
        """
        Initializes menu with background image and areas for displaying texts / buttons / icons.

        Args:
            game (object): Game object.
        """
        self.assets = Assets()
        self.image = self.assets.menu_background
        self.image_rect = self.assets.background_image.get_rect()
        self.game = game

        # 5 Areas that can be filled with content.
        self.center = self.image_rect.center
        self.top = (self.center[0], 65)
        self.bottom = (self.center[0], self.image_rect.height - 65)
        self.left = (self.center[0] // 2, self.center[1])
        self.right = (self.center[0] + self.center[0] // 2, self.center[1])

        # Placeholder for buttons and sliders.
        self.buttons = []
        self.sliders = []

    def display(self, pos=False):
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

        Args:
            event (pygame.event.Event): An occurred pygame event.

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
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
                    return button.name


class MainMenu(Menu):
    """
    Represents the main menu in the game.
    """

    def __init__(self, game):
        """
        Initializes main menu.

        Args:
            game (object): Game object.
        """
        super().__init__(game)
        self.buttons = [
            Button("play_button", self.game.screen, self.center, "magenta", "play", "cyan", self.assets.font_big),
            Button("settings_button", self.game.screen, self.top, "blue", None, None, None,
                   self.assets.settings_icon_small),
            Button("stats_button", self.game.screen, self.left, "cyan", "stats", "dodgerblue", self.assets.font_middle),
            Button("shop_button", self.game.screen, self.right, "cyan", "shop", "dodgerblue", self.assets.font_middle),
            Button("quit_button", self.game.screen, self.bottom, "blue", None, None, None, self.assets.quit_icon)
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

        Returns:
            str: The action based on the button clicked ('play', 'stats', 'settings', 'shop', 'quit').
        """
        clicked_button = super().handle_input(event)
        return clicked_button


class SettingsMenu(Menu):
    """
    Represents the settings menu.
    """

    def __init__(self, game):
        """
        Initializes settings menu.

        Args:
            game (object): Game object.
        """
        super().__init__(game)

        self.sliders = [
            Slider("music_slider", self.game.screen,
                   self.left, (200, 40), self.assets.music.get_volume(), 0, 100, self.assets.font_comicsans_middle),
            Slider("volume_slider", self.game.screen,
                   self.right, (200, 40), self.assets.sounds['shoot'].get_volume(), 0, 100,
                   self.assets.font_comicsans_middle)
        ]
        self.buttons = [
            Button("settings_text", self.game.screen, (self.top[0], self.top[1] + 15), "cyan", "settings",
                   "dodgerblue", self.assets.font_middle),
            Button("settings_icon", self.game.screen, self.center, "blue", None, None, None,
                   self.assets.settings_icon_big),
            Button("back_button", self.game.screen, self.bottom, "cyan", "back", "dodgerblue", self.assets.font_middle)
        ]

    def display(self):
        """
        Displays the menu on the screen.
        """
        super().display()

        # Texts for music and sound volume.
        music_volume = self.assets.font_small.render("Music Volume", True, (0, 255, 255))
        music_volume_rect = music_volume.get_rect(center=(self.left[0] - 100, self.left[1] - 50))
        self.game.screen.blit(music_volume, music_volume_rect)
        sound_volume = self.assets.font_small.render("Sound Volume", True, (0, 255, 255))
        sound_volume_rect = sound_volume.get_rect(center=(self.right[0] + 100, self.right[1] - 50))
        self.game.screen.blit(sound_volume, sound_volume_rect)

        # Update display.
        pygame.display.flip()

    def handle_input(self, event):
        """
        Handles user input for the menu.

        Returns:
            str: The action based on the button clicked ('back').
        """
        # Get values of sliders and update sound / music volume.
        for slider in self.sliders:
            if slider.name == "music_slider":
                self.assets.music.set_volume(round(slider.get_value() / 100, 2))
            elif slider.name == "volume_slider":
                [sound.set_volume(round(slider.get_value() / 100, 2)) for sound in self.assets.sounds.values()]

        clicked_button = super().handle_input(event)
        return clicked_button


class StatsMenu(Menu):
    """
    Represents the statistics menu.
    """

    def __init__(self, game):
        """
        Initializes statistics menu.

        Args:
            game (object): Game object.
        """
        super().__init__(game)

        self.buttons = [
            Button("stats_text", self.game.screen, (self.top[0], self.top[1] + 15), "cyan", "statistics",
                   "dodgerblue", self.assets.font_middle),
            Button("stats_icon", self.game.screen, self.center, "blue", None, None, None, self.assets.stats_icon),
            Button("back_button", self.game.screen, self.bottom, "cyan", "back", "dodgerblue", self.assets.font_middle)
        ]

    def display(self):
        """
        Displays the menu on the screen.
        """
        super().display()

        # Get highscore and travelled distance of last 10 runs .
        highscore, run_distance_df, distance_list = self.get_highscore_and_run_distance()

        # Display dataframe with travelled distance of last 10 runs as table.
        if self.game.number_of_runs > 0:
            self.display_table(run_distance_df)

        # Display highscore.
        highscore_text = self.assets.font_small.render("Highscore", True, "cyan")
        highscore_text_rect = highscore_text.get_rect(center=(self.right[0] + 100, self.right[1] - 70))
        highscore_number = self.assets.font_comicsans_middle.render(str(highscore), True, "dodgerblue")
        highscore_number_rect = highscore_number.get_rect(center=(self.right[0] + 100, self.right[1] - 35))
        self.game.screen.blit(highscore_text, highscore_text_rect)
        self.game.screen.blit(highscore_number, highscore_number_rect)

        # Display average distance of all runs (not only last 10).
        average_text = self.assets.font_small.render("Average Distance", True, "cyan")
        average_text_rect = average_text.get_rect(center=(self.right[0] + 100, self.right[1] + 35))
        if distance_list:
            average = int(np.mean(distance_list))
        else:
            average = 0
        average_number = self.assets.font_comicsans_middle.render(str(average), True, "dodgerblue")
        average_number_rect = average_number.get_rect(center=(self.right[0] + 100, self.right[1] + 70))
        self.game.screen.blit(average_text, average_text_rect)
        self.game.screen.blit(average_number, average_number_rect)

        # Update display.
        pygame.display.flip()

    def get_highscore_and_run_distance(self):
        """
        Gets highscore and distance of last 10 runs.

        Returns:
            highscore (int): The overall highscore.
            run_distance_df (pandas.DataFrame): A pandas DataFrame containing the run number and
                                                distance of the last 10 runs.
            distance_list (list): A list of the last 10 distances.
        """
        # Get highscore and distance of last 10 runs.
        highscore, run_distance_list = self.game.save_load_manager.load_game_data(["highscore", "run_distance"],
                                                                                  [0, [0, 0]])
        run_list = []
        distance_list = []
        distance_list_all = run_distance_list[3::2]
        for index, run_distance in enumerate(run_distance_list[-22:]):
            if index > 1:
                if (index + 1) % 2 == 0:
                    distance_list.append(run_distance)
                else:
                    run_list.append(run_distance)

        # Create DataFrame from distance and run lists for table format.
        run_distance_dict = {"Run": run_list, "Distance": distance_list}
        run_distance_df = pd.DataFrame(run_distance_dict)
        return highscore, run_distance_df, distance_list_all

    def display_table(self, table_df):
        """
        Displays the statistics dataframe as table.

        Args:
            table_df (pandas.DataFrame): A pandas DataFrame containing the data for the table.
        """
        # Cell and table settings
        cell_padding = 5
        cell_height = 40
        cell_width = 150
        table_x, table_y = self.left[0] - 250, self.left[1] - ((table_df.shape[0] + 1) * cell_height / 2)

        # Draw the table columns.
        for i, col in enumerate(table_df.columns):
            cell_rect = pygame.Rect(table_x + i * cell_width, table_y, cell_width, cell_height)
            pygame.draw.rect(self.game.screen, (50, 50, 50), cell_rect)
            cell_text = self.assets.font_comicsans_small.render(col, True, "cyan")
            self.game.screen.blit(cell_text, (cell_rect.x + cell_padding, cell_rect.y + cell_padding))

        # Draw the table rows.
        for i, (_, row) in enumerate(table_df.iterrows()):
            for j, value in enumerate(row):
                cell_rect = pygame.Rect(table_x + j * cell_width, table_y + (i + 1) * cell_height, cell_width,
                                        cell_height)
                pygame.draw.rect(self.game.screen, (100, 100, 100) if i % 2 == 0 else (80, 80, 80), cell_rect)
                cell_text = self.assets.font_comicsans_small.render(str(value), True, "cyan")
                self.game.screen.blit(cell_text, (cell_rect.x + cell_padding, cell_rect.y + cell_padding))

    def handle_input(self, event):
        """
        Handles user input for the menu.

        Returns:
            str: The action based on the button clicked ('back').
        """
        clicked_button = super().handle_input(event)
        return clicked_button


class ShopMenu(Menu):
    """
    Represents the shop menu.
    """

    def __init__(self, game):
        """
        Initializes shop menu.

        Args:
            game (object): Game object.
        """
        super().__init__(game)
        self.shop_warning_insufficient_coins = "Unfortunately you do not have enough coins to purchase this item!"
        self.shop_warning_already_bought = "You already bought this item!"

        self.extra_life_costs = self.assets.config["extra_life_costs"]
        self.weapon_costs = self.assets.config["upgrade_weapon_costs"]
        self.buttons = [
            Button("shop_text", self.game.screen, (self.top[0], self.top[1] + 15), "cyan", "shop",
                   "dodgerblue", self.assets.font_middle),
            Button("shop_icon", self.game.screen, self.center, "blue", None, None, None, self.assets.shop_icon),
            Button("coins_text", self.game.screen, (self.center[0], self.center[1] - 125), "dodgerblue",
                   f"Coins: {self.game.coins}", "cyan", self.assets.font_comicsans_middle),
            Button("heart_icon", self.game.screen, (self.left[0] - 100, self.left[1]), "red",
                   None, None, None, self.assets.heart_icon),
            Button("buy_second_life_button", self.game.screen, (self.left[0] - 100, self.left[1] + 120), "dodgerblue",
                   "buy", "cyan", self.assets.font_small),
            Button("second_life_costs_text", self.game.screen, (self.left[0] - 100, self.left[1] - 90), "dodgerblue",
                   f"Costs: {self.extra_life_costs}", "cyan", self.assets.font_comicsans_middle),
            Button("weapon_icon", self.game.screen, (self.right[0] + 100, self.right[1]), "grey",
                   None, None, None, self.assets.weapon_icon),
            Button("buy_weapon_button", self.game.screen, (self.right[0] + 100, self.right[1] + 120), "dodgerblue",
                   "buy", "cyan", self.assets.font_small),
            Button("weapon_costs_text", self.game.screen, (self.right[0] + 100, self.right[1] - 90), "dodgerblue",
                   f"Costs: {self.weapon_costs}", "cyan", self.assets.font_comicsans_middle),
            Button("back_button", self.game.screen, self.bottom, "cyan", "back", "dodgerblue", self.assets.font_middle)
        ]

    def display(self):
        """
        Displays the menu on the screen.
        """
        super().display()

        # Info text for second life item.
        second_life_info = self.assets.font_comicsans_small.render("Second life for the next run", True, "dodgerblue")
        second_life_info_rect = second_life_info.get_rect(center=(self.left[0] - 100, self.left[1] + 75))
        self.game.screen.blit(second_life_info, second_life_info_rect)

        # Info text for upgrade weapon.
        upgrade_weapon_info_1 = self.assets.font_comicsans_small.render("Upgraded weapon for the next run", True,
                                                                        "dodgerblue")
        upgrade_weapon_info_2 = self.assets.font_comicsans_small.render("(faster and 2 shots)", True,
                                                                        "dodgerblue")
        upgrade_weapon_info_rect1 = upgrade_weapon_info_1.get_rect(center=(self.right[0] + 100, self.right[1] + 50))
        upgrade_weapon_info_rect2 = upgrade_weapon_info_2.get_rect(center=(self.right[0] + 100, self.right[1] + 80))
        self.game.screen.blit(upgrade_weapon_info_1, upgrade_weapon_info_rect1)
        self.game.screen.blit(upgrade_weapon_info_2, upgrade_weapon_info_rect2)

        # Update display.
        pygame.display.flip()

    def handle_input(self, event):
        """
        Handles user input for the menu.

        Returns:
            str: The action based on the button clicked ('back', 'buy_second_life', 'buy_weapon').
        """
        clicked_button = super().handle_input(event)
        return clicked_button


class GameOverMenu(Menu):
    """
    Represents the game over menu.
    """

    def __init__(self, game):
        """
        Initializes game over menu.

        Args:
            game (object): Game object.
        """
        super().__init__(game)

        # Load different background image for game over screen.
        self.image = self.assets.game_over_image

        self.buttons = [
            Button("main_menu_button", self.game.screen, (self.left[0], self.bottom[1]), "dodgerblue", "main menu",
                   "dodgerblue", self.assets.font_small),
            Button("restart_button", self.game.screen, (self.center[0], self.bottom[1]), "green",
                   "restart", "green",
                   self.assets.font_small),
            Button("quit_button", self.game.screen, (self.right[0], self.bottom[1]), "red",
                   "quit", "red",
                   self.assets.font_small)
        ]

    def display(self):
        """
        Displays the menu on the screen.
        """
        super().display(True)

        # Travelled distance text.
        distance = self.assets.font_comicsans_big.render(f"Distance: {self.game.distance}", True, "cyan")
        distance_rect = distance.get_rect(center=(self.center[0], 50))
        self.game.screen.blit(distance, distance_rect)

        # Highscore text.
        highscore = self.assets.font_comicsans_big.render(f"Highscore: {self.game.highscore}", True, "cyan")
        highscore_rect = highscore.get_rect(center=(self.left[0] - 100, 50))
        self.game.screen.blit(highscore, highscore_rect)

        # Achieved coins text.
        coins = self.assets.font_comicsans_big.render(f"Coins: {int(self.game.distance / 100)}", True, "cyan")
        coins_rect = coins.get_rect(center=(self.right[0] + 100, 50))
        self.game.screen.blit(coins, coins_rect)

        # Explanation text for restarting.
        exp_text = self.assets.font_small.render("Press space or klick restart button to try again", True, "aqua")
        exp_text_rect = exp_text.get_rect(center=(self.center[0], self.center[1] + 245))
        self.game.screen.blit(exp_text, exp_text_rect)

        # Update display.
        pygame.display.flip()

    def handle_input(self, event):
        """
        Handles user input for the menu.

        Returns:
            str: The action based on the button clicked ('restart', 'main_menu', 'quit').
        """
        clicked_button = super().handle_input(event)
        return clicked_button


class PauseMenu(Menu):
    """
    Represents the pause menu.
    """

    def __init__(self, game):
        """
        Initializes pause menu.

        Args:
            game (object): Game object.
        """
        super().__init__(game)

        # Load different background image for pause screen.
        self.image = self.assets.pause_image

        self.buttons = [
            Button("resume_button", self.game.screen, (self.image_rect.centerx, 275), "green", "resume", "green",
                   self.assets.font_small),
            Button("main_menu_button", self.game.screen, (self.image_rect.centerx, 375), "dodgerblue", "main menu",
                   "dodgerblue", self.assets.font_small),
            Button("quit_button", self.game.screen, (self.image_rect.centerx, 475), "red", "quit", "red",
                   self.assets.font_small)
        ]

    def display(self):
        """
        Displays the menu on the screen.
        """
        super().display(True)

        # Paused text.
        paused = self.assets.font_middle.render("paused", True, "cyan")
        self.game.screen.blit(paused, (self.image_rect.centerx - paused.get_width() // 2, 100))

        # Update display.
        pygame.display.flip()

    def handle_input(self, event):
        """
        Handles user input for the menu.

        Returns:
            str: The action based on the button clicked ('resume', 'main_menu', 'quit').
        """
        clicked_button = super().handle_input(event)
        return clicked_button


class Slider:
    """
    Class representing slider UI elements.
    """

    def __init__(self, name, screen, pos, size, initial_val, min, max, font):
        """
        Initializes a slider.
        """
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
        """
        Moves slider to the position of the mouse.

        Args:
            mouse_pos (tuple): X and y coordinates of the mouse position.
        """
        pos = mouse_pos[0]
        if pos < self.slider_left_pos:
            pos = self.slider_left_pos
        if pos > self.slider_right_pos:
            pos = self.slider_right_pos
        self.button_rect.centerx = pos

    def hover(self):
        """
        Sets hover state.
        """
        self.hovered = True

    def render(self):
        """
        Renders the slider to the screen.
        """
        pygame.draw.rect(self.screen, "darkgray", self.container_rect)
        pygame.draw.rect(self.screen, self.button_states[self.hovered], self.button_rect)

    def get_value(self):
        """
        Gets the value of the current button position in the slider.

        Returns:
            percentage (int): The percentage of the button position relative to the slider size.
        """
        val_range = self.slider_right_pos - self.slider_left_pos - 1
        button_val = self.button_rect.centerx - self.slider_left_pos
        percentage = (button_val / val_range) * (self.max - self.min) + self.min

        return percentage

    def display_value(self):
        """
        Display the value in a label above the slider.
        """
        self.text = self.font.render(str(int(self.get_value())), True, "white")
        self.screen.blit(self.text, self.label_rect)


class Button:
    """
    Class representing button UI elements.
    """

    def __init__(self, name, screen, position, border_color, text, text_color, font, image=None):
        """
        Initializes a button.
        """
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

        # Get button rect and draw button on screen.
        self.rect = button.get_rect(center=self.position)
        pygame.draw.rect(self.screen, self.border_color, self.rect.inflate(30, 10), 5, border_radius=25)
        self.screen.blit(button, (self.rect.x, self.rect.y))

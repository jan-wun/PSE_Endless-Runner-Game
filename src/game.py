import pygame
import sys
import random
from tkinter import messagebox
from src.assets import Assets
from src.enums import GameState, EnemyType, WeaponType, PowerUpType
from src.menu import GameOverMenu, PauseMenu, SettingsMenu, MainMenu, StatsMenu, ShopMenu, ControlsMenu
from src.manager import SaveLoadSystem
from src.player import Player
from src.obstacle import Obstacle
from src.enemy import Enemy
from src.weapon import Weapon
from src.powerup import PowerUp
from src.projectile import Projectile


class Game:
    """
    The main class representing the endless runner game.
    """

    def __init__(self, size):
        """
        Initializes the Game object.

        This method sets up the Pygame environment, display, data, variables, menus, audio, timers and sprite groups.
        Args:
            size (list): The size of the game window ([width, height]).
        """
        # Initialize Pygame.
        pygame.init()

        # Set up the display.
        self.width = size[0]
        self.height = size[1]
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Run the Cybernetic City: Endless Dash")

        # Load assets.
        self.assets = Assets()

        # Initialize save load manager.
        self.save_load_manager = SaveLoadSystem(".save", "data")

        # Load data from previous game sessions or set default values.
        self.coins = self.save_load_manager.load_game_data(["coins"], [0])
        self.number_of_runs = self.save_load_manager.load_game_data(["run_distance"], [[0, 0]])[-2]
        self.highscore = self.save_load_manager.load_game_data(["highscore"], [0])
        self.assets.music.set_volume(self.save_load_manager.load_game_data(["volume"], [(0.1, 0.3)])[0])
        [sound.set_volume(self.save_load_manager.load_game_data(["volume"], [(0.1, 0.3)])[1]) for sound in
         self.assets.sounds.values()]

        # Initialize different menus and define pause button.
        self.main_menu = MainMenu(self)
        self.stats_menu = StatsMenu(self)
        self.shop_menu = ShopMenu(self)
        self.settings_menu = SettingsMenu(self)
        self.controls_menu = ControlsMenu(self)
        self.game_over_menu = GameOverMenu(self)
        self.pause_menu = PauseMenu(self)
        self.pause_button_rect = self.assets.pause_button_image.get_rect(
            topright=(self.width - 10, 10))
        self.pause_button_clicked = False

        # Initialize background position and scrolling speed.
        self.background_x = 0
        self.scrolling_bg_speed = self.assets.config["scrolling_bg_speed"]

        # Set fps for game.
        self.fps = self.assets.config["fps"]

        # Set variables for current run.
        self.set_up_run()

        self.shrink_timer = 0  # Timer für Shrink-Power-Up

        # Initialize and set timers for background speed, obstacle, enemy and power up objects.
        self.obstacle_timer = pygame.USEREVENT + 1
        self.enemy_timer = pygame.USEREVENT + 2
        self.power_up_timer = pygame.USEREVENT + 3
        self.background_speed_timer = pygame.USEREVENT + 4
        pygame.time.set_timer(self.obstacle_timer, self.assets.config["obstacle_timer"] * 1000)
        pygame.time.set_timer(self.enemy_timer, self.assets.config["enemy_timer"] * 1000)
        pygame.time.set_timer(self.power_up_timer, self.assets.config["power_up_timer"] * 1000)
        pygame.time.set_timer(self.background_speed_timer, self.assets.config["bg_speed_timer"] * 1000)

        # Create sprite group single for player and add player.
        self.player = pygame.sprite.GroupSingle()
        self.player.add(Player(self.assets.player_idle, self.assets.player_walk, self.assets.player_jump,
                               self.assets.player_slide, self))

        # Create sprite groups for other entities (obstacles, enemies, power ups and projectiles).
        self.obstacles = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.power_ups = pygame.sprite.Group()
        self.projectiles = pygame.sprite.Group()

    def set_up_run(self, startup=True):
        """
        Sets the variables for the game startup.

        Args:
            startup (bool): Whether the function is executed at startup or not.
        """
        # Initialize distance and background speed for current run.
        self.distance = 0
        self.scrolling_bg_speed = self.assets.config["scrolling_bg_speed"]
        # Variables for freeze power up.
        self.freeze = False
        self.freeze_time = self.fps * self.assets.config["freeze_time"]
        # Flag whether data has already been updated for current run.
        self.updated_data = False
        # The main menu should only be shown on startup.
        self.current_state = GameState.MAIN_MENU if startup else GameState.PLAYING

    def start_game(self):
        """
        Starts the main game loop in which the game logic takes place.
        """
        # Create a clock object to control the frame rate.
        clock = pygame.time.Clock()

        # Play background music.
        self.assets.music.play(-1)

        # Main Game loop.
        while True:
            # Loop over events from queue.
            for event in pygame.event.get():
                # Handle different GameStates and events.
                self.handle_states_and_events(event)

            # Update and render all game objects when game state is playing.
            if self.current_state == GameState.PLAYING:
                self.update()
                self.render()

            # Update and save data of run and how game over screen when game state is game over.
            elif self.current_state == GameState.GAME_OVER:
                self.update_and_save_run_data()
                self.game_over_menu.display()

            # Cap the frame rate to defined fps.
            clock.tick(self.fps)

    def handle_states_and_events(self, event):
        """
        Processes game states and various events such as exiting the game or pressing a mouse/keyboard button.

        Args:
            event (pygame.event.Event): An event that has occurred.
        """
        # Handle quitting game (via ESC key or close button).
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            self.end_game()
        # Handle game over state, display menu and check which button player clicks (restart, main_menu, quit).
        if self.current_state == GameState.GAME_OVER:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.restart_game()
            self.handle_button_result(self.game_over_menu.handle_input(event))
        # Handle paused state, display menu and check which button player clicks (resume, main_menu, quit).
        elif self.current_state == GameState.PAUSED:
            self.pause_menu.display()
            self.handle_button_result(self.pause_menu.handle_input(event))
        # Handle main menu state, display menu and check which button player clicks (play, settings, quit, shop, stats).
        elif self.current_state == GameState.MAIN_MENU:
            self.main_menu.display()
            self.handle_button_result(self.main_menu.handle_input(event))
        # Handle settings state, display menu and check whether player changes settings.
        elif self.current_state == GameState.SETTINGS:
            self.settings_menu.display()
            self.handle_button_result(self.settings_menu.handle_input(event))
        # Handle shop state, display menu and check whether player buys something.
        elif self.current_state == GameState.SHOP:
            self.shop_menu.display()
            self.handle_button_result(self.shop_menu.handle_input(event))
        # Handle controls state, display menu and check for player clicks (back button).
        elif self.current_state == GameState.CONTROLS:
            self.controls_menu.display()
            self.handle_button_result(self.controls_menu.handle_input(event))
        # Handle stats state, display menu and check for player clicks (back button).
        elif self.current_state == GameState.STATS:
            self.stats_menu.display()
            self.handle_button_result(self.stats_menu.handle_input(event))
        # Handle playing state.
        elif self.current_state == GameState.PLAYING:
            # Check whether pause button or key (p) is clicked and pause game accordingly.
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and
                self.pause_button_rect.collidepoint(mouse_x, mouse_y)) or event.type == pygame.KEYDOWN and \
                    event.key == pygame.K_p:
                self.pause_button_clicked = True
            elif (event.type == pygame.KEYUP and event.key == pygame.K_p) or (
                    (event.type == pygame.MOUSEBUTTONUP and event.button == 1 and
                     self.pause_button_rect.collidepoint(mouse_x, mouse_y)) and self.pause_button_clicked):
                self.pause_button_clicked = False
                self.current_state = GameState.PAUSED
            # Only add obstacles and enemies when game is not frozen.
            if not self.freeze:
                # Check obstacle timer and add car or meteor to obstacles.
                if event.type == self.obstacle_timer:
                    self.obstacles.add(random.choice([Obstacle([self.width + random.randint(200, 500), 480],
                                                               [pygame.transform.flip(image, True, False) for image
                                                                in self.assets.car_images], 'car', 5, self),
                                                      Obstacle([self.width + random.randint(200, 500), 585],
                                                               self.assets.meteor_images, 'meteor', 0, self)]))
                # Check enemy timer and add drone or robot to enemies.
                elif event.type == self.enemy_timer:
                    enemy_choice = random.choice([EnemyType.DRONE, EnemyType.ROBOT])
                    if not any(enemy.type == enemy_choice for enemy in self.enemies):
                        enemy_position = [1500, 100] if enemy_choice == EnemyType.DRONE else [1500, 512]
                        self.enemies.add(Enemy(enemy_position, enemy_choice, self))
                # Check powerup timer and add a random powerup object to powerups.
                elif event.type == self.power_up_timer:
                    # Multiple_shots are only added to the random selection if the player has not collected them yet.
                    power_up_list = [PowerUpType.INVINCIBILITY, PowerUpType.FREEZE]
                    if not self.player.sprite.weapon.max_shots == self.assets.config["multiple_shots"]:
                        power_up_list.append(PowerUpType.MULTIPLE_SHOTS)
                    power_up_choice = random.choice(power_up_list)
                    self.power_ups.add(PowerUp([1500, 0], power_up_choice, self))
                # Check background speed timer and increase scrolling background speed.
                elif event.type == self.background_speed_timer:
                    self.scrolling_bg_speed += self.assets.config["bg_speed_increase"]

    def update(self):
        """
        Updates all game objects.
        """
        # Update player.
        self.player.update()

        # Check whether freeze powerup was collected and game is frozen.
        if self.freeze:
            if self.freeze_time > 0:
                self.freeze_time -= 1
            else:
                self.freeze = False
                self.freeze_time = self.fps * self.assets.config["freeze_time"]
        else:
            # Update all objects in every sprite group (obstacles, enemies, power ups, projectiles).
            self.obstacles.update()
            self.enemies.update()
            self.projectiles.update()
            self.power_ups.update()

            # Scroll background to the left.
            self.background_x -= self.scrolling_bg_speed
            # Check if the background has scrolled off the screen and reset position.
            if self.background_x <= -self.width:
                self.background_x = 0

        if self.shrink_timer > 0:
            self.shrink_timer -= 1
            if self.shrink_timer == 0:
                self.reset_shrink_effect()

        # Check for collisions between different game objects and handle them accordingly.
        self.check_collision(self.player.sprite, self.obstacles)
        self.check_collision(self.player.sprite, self.enemies)
        self.check_collision(self.player.sprite, self.projectiles)
        [self.check_collision(enemy, self.projectiles) for enemy in self.enemies]
        self.check_collision(self.player.sprite, self.power_ups)

        # Update distance.
        self.distance += 1

    def reset_shrink_effect(self):
        """Resets the shrink effect when the timer expires."""
        self.player.sprite.scale_factor = 1.0
        self.player.sprite.rect.width = self.player.sprite.original_width
        self.player.sprite.rect.height = self.player.sprite.original_height
        self.player.sprite.position[1] -= (self.player.sprite.original_height * 0.75)  # Reposition to normal

        self.player.sprite.weapon.scale_factor = 1.0
        self.player.sprite.weapon.rect.width = self.player.sprite.weapon.original_width
        self.player.sprite.weapon.rect.height = self.player.sprite.weapon.original_height

    def render(self):
        """
        Renders all game objects to the screen.
        """
        # Draw the background image with scroll position.
        self.screen.blit(self.assets.background_image, (self.background_x, 0))
        # Create seamless scrolling effect.
        self.screen.blit(self.assets.background_image, (self.background_x + self.width, 0))

        # Display current score on screen.
        distance_surface = self.assets.font_comicsans_big.render(f"Score: {self.distance}", True, "green")
        self.screen.blit(distance_surface, (10, 10))

        # Display pause button in the top right corner.
        self.screen.blit(self.assets.pause_button_image, self.pause_button_rect)

        # Draw player and weapon.
        self.player.draw(self.screen)
        self.screen.blit(self.player.sprite.weapon.image, self.player.sprite.weapon.position)

        # Draw all sprites in the sprite groups (obstacles, enemies, power ups, projectiles).
        self.obstacles.draw(self.screen)
        self.enemies.draw(self.screen)
        self.power_ups.draw(self.screen)
        self.projectiles.draw(self.screen)

        # Display number of player lifes.
        self.screen.blit(self.assets.font_comicsans_big.render(f"Lifes: {self.player.sprite.health}", True, "cyan"),
                         (10, 60))

        # Draw icons for power ups on the screen.
        self.display_power_ups()

        # Display slide cooldown time on the screen.
        self.screen.blit(self.assets.font_comicsans_small.render(
            f"Slide Cooldown: {round(self.player.sprite.slide_cooldown / self.fps, 1)}", True, "cyan"), (self.width - 220, 80))

        # Update the full display Surface to the screen.
        pygame.display.flip()

    def update_and_save_run_data(self):
        """
        Updates and saves data for the current run.
        """
        # Update highscore if necessary.
        if self.distance > self.highscore:
            self.highscore = self.distance

        # If the data for the current run has not yet been updated, update it.
        if not self.updated_data:
            self.updated_data = True
            # Update number of runs.
            self.number_of_runs += 1
            # Update coins.
            self.coins += int(self.distance / 100)
            # Re-instantiate shop for updated coins.
            self.shop_menu = ShopMenu(self)
            # Save data of run.
            self.save_load_manager.save_game_data([
                [self.number_of_runs, self.distance], self.highscore, self.coins],
                ["run_distance", "highscore", "coins"],
                ["ab", "wb", "wb"])

    def end_game(self):
        """
        Quits the game and saves audio settings and data from last attempt.
        """
        # Save game data and volume settings of music and sounds.
        self.save_load_manager.save_game_data(
            [(self.assets.music.get_volume(), self.assets.sounds["shoot"].get_volume()), self.highscore, self.coins],
            ["volume", "highscore", "coins"], ["wb", "wb", "wb"])

        # Close game and window.
        pygame.quit()
        sys.exit()

    def reset_timers(self):
        """
        Resets timers for obstacles, enemies, and power-ups.
        """
        pygame.time.set_timer(self.obstacle_timer, self.assets.config["obstacle_timer"] * 1000)
        pygame.time.set_timer(self.enemy_timer, self.assets.config["enemy_timer"] * 1000)
        pygame.time.set_timer(self.power_up_timer, self.assets.config["power_up_timer"] * 1000)
        pygame.time.set_timer(self.background_speed_timer, self.assets.config["bg_speed_timer"] * 1000)

    def restart_game(self):
        """
        Restarts the game.
        """
        # Kill all obstacles, enemies, projectiles and powerups.
        [obstacle.kill() for obstacle in self.obstacles]
        [enemy.kill() for enemy in self.enemies]
        [projectile.kill() for projectile in self.projectiles]
        [power_up.kill() for power_up in self.power_ups]

        # Reset the player.
        self.player.sprite.reset()

        # Reset variables for next run.
        self.set_up_run(False)

        # Reset timers.
        self.reset_timers()

        # Re-instantiate shop for updated coins.
        self.shop_menu = ShopMenu(self)

    def handle_button_result(self, result):
        """
        Handles what should happen when a specific button is clicked.

        Args
            result (str): String representing the name of the clicked button.
        """
        if result == "resume_button":
            self.current_state = GameState.PLAYING
        elif result == "restart_button":
            self.current_state = GameState.PLAYING
            self.restart_game()
        elif result == "play_button":
            self.current_state = GameState.PLAYING
            health = self.player.sprite.health
            weapon = self.player.sprite.weapon
            self.restart_game()
            self.player.sprite.health = health
            self.player.sprite.weapon = weapon

        elif result == "settings_button":
            self.current_state = GameState.SETTINGS
        elif result == "shop_button":
            self.current_state = GameState.SHOP
        elif result == "stats_button":
            self.current_state = GameState.STATS
        elif result == "controls_button":
            self.current_state = GameState.CONTROLS
        elif result == "main_menu_button":
            self.current_state = GameState.MAIN_MENU
            self.player.sprite.reset()
        elif result == "back_button":
            self.current_state = GameState.MAIN_MENU
        elif result == "buy_second_life_button":
            self.handle_shop_purchase(self.shop_menu.extra_life_costs, "extra_life")
        elif result == "buy_weapon_button":
            self.handle_shop_purchase(self.shop_menu.weapon_costs, "weapon_upgrade")
        elif result == "quit_button":
            self.end_game()

    def check_collision(self, sprite, sprite_group):
        """
        Checks for collision between a single sprite and a sprite group.

        Args:
            sprite (pygame.sprite.Sprite): The sprite used to check for collisions.
            sprite_group (pygame.sprite.Group): The sprite group used to check for collisions.
        """
        # Check whether sprite collides with any sprite in sprite group.
        hit_sprite = pygame.sprite.spritecollideany(sprite, sprite_group)
        if hit_sprite:
            # Check whether the sprite is an enemy.
            if isinstance(sprite, Enemy):
                # Kill the enemy and the sprite it hit and return a shot to the player.
                sprite.kill()
                hit_sprite.kill()
                self.player.sprite.weapon.shots += 1
            # Check whether the sprite is the player.
            elif isinstance(sprite, Player):
                # Check whether a power up collided with the player.
                if isinstance(hit_sprite, PowerUp):
                    # Apply power up and kill it.
                    hit_sprite.apply_powerup()
                    hit_sprite.kill()
                elif isinstance(hit_sprite, Projectile):
                    if hit_sprite.shooter != "player":
                        self.handle_player_collision()
                else:
                    self.handle_player_collision()

    def handle_player_collision(self):
        """
        Handles player collision.
        """
        # Check whether player is invincible.
        if not self.player.sprite.invincible:
            # Decrease player health.
            self.player.sprite.health -= 1
            # Check whether player has no lives.
            if self.player.sprite.health == 0:
                # Set game state to game over.
                self.current_state = GameState.GAME_OVER
            else:
                # Kill obstacles, enemies and projectiles and let player continue run.
                [obstacle.kill() for obstacle in self.obstacles]
                [enemy.kill() for enemy in self.enemies]
                [projectile.kill() for projectile in self.projectiles]

    def handle_shop_purchase(self, item_costs, item_name):
        """
        Processes store purchases and displays warning messages if a store item could not be purchased.

        Args:
            item_costs (int): The amount of coins an item costs.
            item_name (string): The name of an item.
        """
        # Display insufficient_coins message when user has not enough coins.
        if self.coins < item_costs:
            messagebox.showinfo(title="Shop-Warning", message=self.shop_menu.shop_warning_insufficient_coins)
        else:
            # Process purchase of the clicked item.
            if item_name == "extra_life":
                self.handle_extra_life_purchase(item_costs)
            else:
                self.handle_weapon_upgrade_purchase(item_costs)

        # Re-instantiate shop for updated coins.
        self.shop_menu = ShopMenu(self)

    def handle_extra_life_purchase(self, item_costs):
        """
        Processes purchases of the extra life item.

        Args:
            item_costs (int): The amount of coins the item costs.
        """
        # Check whether player already bought the extra life item.
        if self.player.sprite.health != 2:
            # Subtract costs of item from coins and update player health.
            self.coins -= item_costs
            self.player.sprite.health = 2
        else:
            # Show warning message.
            messagebox.showinfo(title="Shop-Warning", message=self.shop_menu.shop_warning_already_bought)

    def handle_weapon_upgrade_purchase(self, item_costs):
        """
        Processes purchases of the weapon upgrade item.

        Args:
            item_costs (int): The amount of coins the item costs.
            already_bought_script (str): A string containing the message that the item has already been purchased.
        """
        # Check whether player already bought the weapon upgrade item.
        if self.player.sprite.weapon.type != WeaponType.UPGRADE:
            # Subtract costs of item from coins and update weapon.
            self.coins -= item_costs
            self.player.sprite.weapon.kill()
            self.player.sprite.weapon = Weapon(
                [self.player.sprite.position[0] + self.player.sprite.rect.width, self.player.sprite.position[1] + 30],
                WeaponType.UPGRADE, self, self.player.sprite)
        else:
            # Show warning message.
            messagebox.showinfo(title="Shop-Warning", message=self.shop_menu.shop_warning_already_bought)

    def display_power_ups(self):
        """
        Displays power ups on screen. If they are grey, they are not active.
        """
        for power_up_type in PowerUpType:
            time_left = ""
            if power_up_type == PowerUpType.MULTIPLE_SHOTS:
                if self.player.sprite.weapon.max_shots == self.assets.config["multiple_shots"]:
                    image = self.assets.multiple_shots_power_up
                    time_left = u"\u221E"
                else:
                    image = self.assets.multiple_shots_power_up_inactive
                height = 120
            if power_up_type == PowerUpType.FREEZE:
                if self.freeze:
                    image = self.assets.freeze_powerup
                    time_left = round(self.freeze_time / self.fps, 1)
                else:
                    image = self.assets.freeze_powerup_inactive
                height = 190
            if power_up_type == PowerUpType.INVINCIBILITY:
                if self.player.sprite.invincible:
                    image = self.assets.invincible_powerup
                    time_left = round(self.player.sprite.invincible_time / self.fps, 1)
                else:
                    image = self.assets.invincible_powerup_inactive
                height = 260
            self.screen.blit(image[0], (self.width - 70, height))
            self.screen.blit(self.assets.font_comicsans_small.render(str(time_left), True, "cyan"),
                             (self.width - 105, height + 15))

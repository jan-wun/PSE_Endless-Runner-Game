import json
import os
import pygame


class Assets(object):
    """
    Singleton class for managing game assets.
    """
    # Class attribute to store the singleton instance.
    _instance = None

    def __new__(cls):
        """
        Create a new instance if it doesn't exist, and load assets.
        """
        if not cls._instance:
            # Create a new instance using the parent class's __new__ method.
            cls._instance = super(Assets, cls).__new__(cls)
            # Load assets when creating the instance.
            cls._instance.load_assets()
        # Return the existing or newly created instance.
        return cls._instance

    def load_assets(self):
        """
        Load game assets.
        """
        # Load configuration parameter from config file.
        self.load_config()
        audio_path = self.config["audio_path"]
        font_path = self.config["font_path"]
        image_path = self.config["image_path"]

        # Load all images required for the game.
        # Images for background and pause button.
        self.background_image = pygame.image.load(os.path.join(image_path, "background.png")).convert_alpha()
        self.pause_button_image = pygame.transform.scale_by(
            pygame.image.load(os.path.join(image_path, "icons/pause_button.png")).convert_alpha(), 0.25)

        # Images for player.
        self.player_idle = [pygame.transform.scale_by(
            pygame.image.load(os.path.join(image_path, f"player/idle/idle{i}.png")).convert_alpha(), 4) for i in
            range(1, 5)]
        self.player_walk = [pygame.transform.scale_by(
            pygame.image.load(os.path.join(image_path, f"player/walk/walk{i}.png")).convert_alpha(), 4) for i in
            range(1, 7)]
        self.player_jump = [pygame.transform.scale_by(
            pygame.image.load(os.path.join(image_path, f"player/jump/jump{i}.png")).convert_alpha(), 4) for i in
            range(1, 5)]
        self.player_slide = [pygame.transform.scale_by(
            pygame.image.load(os.path.join(image_path, f"player/slide/slide{i}.png")).convert_alpha(), 4) for i in
            range(1, 2)]

        # Images for obstacles.
        self.car_images = [
            pygame.transform.scale_by(pygame.image.load(os.path.join(image_path, "obstacles/car.png")).convert_alpha(),
                                      1.5)]
        self.meteor_images = [
            pygame.transform.scale_by(
                pygame.image.load(os.path.join(image_path, "obstacles/meteor.png")).convert_alpha(), 0.25)]

        # Images for enemies.
        self.drone_images = [pygame.transform.scale_by(
            pygame.image.load(os.path.join(image_path, f"enemies/drone/idle/idle{i}.png")).convert_alpha(), 3) for i in
            range(1, 5)]
        self.capsule_image = pygame.transform.scale_by(
            pygame.image.load(os.path.join(image_path, "bullets/capsule.png")).convert_alpha(),
            1.5)
        self.robot_images = [pygame.transform.scale_by(
            pygame.image.load(os.path.join(image_path, f"enemies/robot/idle/idle{i}.png")).convert_alpha(), 3) for i in
            range(1, 5)]
        self.projectile_image = pygame.transform.scale_by(
            pygame.image.load(os.path.join(image_path, "bullets/projectile.png")).convert_alpha(),
            1.5)

        # Images for menus.
        self.menu_background = pygame.transform.scale(
            pygame.image.load(os.path.join(image_path, "menu.png")).convert_alpha(),
            (1344, 768))
        self.game_over_image = pygame.transform.scale_by(
            pygame.image.load(os.path.join(image_path, "game_over.png")).convert_alpha(), 0.5)
        self.pause_image = pygame.transform.scale_by(
            pygame.image.load(os.path.join(image_path, "pause.png")).convert_alpha(), 0.15)
        self.settings_icon_big = pygame.transform.scale_by(
            pygame.image.load(os.path.join(image_path, "icons/settings.png")).convert_alpha(), 0.6)
        self.settings_icon_small = pygame.transform.scale_by(self.settings_icon_big, 0.5)
        self.quit_icon = pygame.transform.scale_by(
            pygame.image.load(os.path.join(image_path, "icons/quit.png")).convert_alpha(), 0.15)
        self.stats_icon = pygame.transform.scale_by(
            pygame.image.load(os.path.join(image_path, "icons/statistics.png")).convert_alpha(),
            0.2)
        self.shop_icon = pygame.transform.scale_by(
            pygame.image.load(os.path.join(image_path, "icons/shopping_cart.png")).convert_alpha(),
            0.05)
        self.heart_icon = pygame.transform.scale_by(
            pygame.image.load(os.path.join(image_path, "icons/heart.png")).convert_alpha(),
            0.03)
        self.weapon_icon = pygame.transform.scale_by(
            pygame.image.load(os.path.join(image_path, "player/weapon/weapon2_right.png")).convert_alpha(), 5)

        # Images for power ups.
        self.invincible_powerup = [
            pygame.transform.scale(
                pygame.image.load(os.path.join(image_path, "power_ups/invincible.png")).convert_alpha(),
                (56, 56))]
        self.invincible_powerup_inactive = [
            pygame.transform.scale(
                pygame.image.load(os.path.join(image_path, "power_ups/invincible_inactive.png")).convert_alpha(),
                (56, 56))]
        self.freeze_powerup = [
            pygame.transform.scale(pygame.image.load(os.path.join(image_path, "power_ups/freeze.png")).convert_alpha(),
                                   (56, 56))]
        self.freeze_powerup_inactive = [
            pygame.transform.scale(
                pygame.image.load(os.path.join(image_path, "power_ups/freeze_inactive.png")).convert_alpha(),
                (56, 56))]
        self.multiple_shots_power_up = [pygame.transform.scale(
            pygame.image.load(os.path.join(image_path, "power_ups/multiple_shots.png")).convert_alpha(), (56, 56))]
        self.multiple_shots_power_up_inactive = [pygame.transform.scale(
            pygame.image.load(os.path.join(image_path, "power_ups/multiple_shots_inactive.png")).convert_alpha(),
            (56, 56))]

        # Images for weapon.
        self.default_weapon_bullet = pygame.transform.scale_by(
            pygame.image.load(os.path.join(image_path, "bullets/default_weapon.png")).convert_alpha(), 3)
        self.default_weapon_images = [pygame.transform.scale_by(
            pygame.image.load(os.path.join(image_path, "player/weapon/weapon1_right.png")).convert_alpha(), 2.5),
            pygame.transform.scale_by(
                pygame.image.load(os.path.join(image_path, "player/weapon/weapon1_left.png")).convert_alpha(), 2.5)]
        self.upgrade_weapon_bullet = pygame.transform.scale_by(
            pygame.image.load(os.path.join(image_path, "bullets/upgrade_weapon.png")).convert_alpha(), 3)
        self.upgrade_weapon_images = [pygame.transform.scale_by(
            pygame.image.load(os.path.join(image_path, "player/weapon/weapon2_right.png")).convert_alpha(), 2.5),
            pygame.transform.scale_by(
                pygame.image.load(os.path.join(image_path, "player/weapon/weapon2_left.png")).convert_alpha(), 2.5)]

        # Load all audio data required for the game.
        self.music = pygame.mixer.Sound(os.path.join(audio_path, "music.mp3"))
        self.sounds = {
            "click": pygame.mixer.Sound(os.path.join(audio_path, "click.mp3")),
            "jump": pygame.mixer.Sound(os.path.join(audio_path, "jump.mp3")),
            "shoot": pygame.mixer.Sound(os.path.join(audio_path, "shoot.mp3"))
        }

        # Load all fonts required for the game.
        self.font_big = pygame.font.Font(os.path.join(font_path, "stacker.ttf"), 100)
        self.font_middle = pygame.font.Font(os.path.join(font_path, "stacker.ttf"), 60)
        self.font_small = pygame.font.Font(os.path.join(font_path, "stacker.ttf"), 30)
        self.font_comicsans_big = pygame.font.SysFont("comicsans", 40)
        self.font_comicsans_middle = pygame.font.SysFont("comicsans", 30)
        self.font_comicsans_small = pygame.font.SysFont("comicsans", 22)

    def load_config(self):
        with open('config.json', 'r') as file:
            self.config = json.load(file)

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
        Load game assets using a JSON configuration.
        """
        self.load_config()
        audio_path = self.config["audio_path"]
        font_path = self.config["font_path"]
        image_path = self.config["image_path"]

        def load_image(path, scale=1):
            """Helper function to load and scale images."""
            image = pygame.image.load(os.path.join(image_path, path)).convert_alpha()
            return pygame.transform.scale_by(image, scale) if scale != 1 else image

        with open(os.path.join(image_path, "assets_config.json"), "r") as file:
            asset_definitions = json.load(file)

        self.images = {}
        for key, asset in asset_definitions.items():
            self.images[key] = load_image(asset["path"], asset.get("scale", 1))

        # Load audio
        self.sounds = {name: pygame.mixer.Sound(os.path.join(audio_path, f"{name}.mp3")) for name in
                       ["click", "jump", "shoot"]}
        self.music = pygame.mixer.Sound(os.path.join(audio_path, "music.mp3"))

        # Load fonts
        self.fonts = {
            "big": pygame.font.Font(os.path.join(font_path, "stacker.ttf"), 100),
            "middle": pygame.font.Font(os.path.join(font_path, "stacker.ttf"), 60),
            "small": pygame.font.Font(os.path.join(font_path, "stacker.ttf"), 30)
        }

    def load_config(self):
        with open('config.json', 'r') as file:
            self.config = json.load(file)

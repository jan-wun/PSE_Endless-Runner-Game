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
        Load game assets using a JSON configuration while maintaining full compatibility and correct scaling.
        """
        self.load_config()
        audio_path = self.config["audio_path"]
        font_path = self.config["font_path"]
        image_path = self.config["image_path"]

        def load_image(path, scale=None, fixed_size=None):
            """Helper function to load and scale images correctly."""
            image = pygame.image.load(os.path.join(image_path, path)).convert_alpha()
            if fixed_size:
                return pygame.transform.scale(image, fixed_size)
            if scale:
                return pygame.transform.scale_by(image, scale)
            return image

        with open(os.path.join(image_path, "assets_config.json"), "r") as file:
            asset_definitions = json.load(file)

        # Load all images while applying correct scaling
        for attr, asset in asset_definitions.items():
            if isinstance(asset, list):
                setattr(self, attr,
                        [load_image(entry["path"], entry.get("scale"), entry.get("fixed_size")) for entry in asset])
            else:
                setattr(self, attr, load_image(asset["path"], asset.get("scale"), asset.get("fixed_size")))

        # Load audio
        self.music = pygame.mixer.Sound(os.path.join(audio_path, "music.mp3"))
        self.sounds = {
            "click": pygame.mixer.Sound(os.path.join(audio_path, "click.mp3")),
            "jump": pygame.mixer.Sound(os.path.join(audio_path, "jump.mp3")),
            "shoot": pygame.mixer.Sound(os.path.join(audio_path, "shoot.mp3"))
        }

        # Load fonts
        self.font_big = pygame.font.Font(os.path.join(font_path, "stacker.ttf"), 100)
        self.font_middle = pygame.font.Font(os.path.join(font_path, "stacker.ttf"), 60)
        self.font_small = pygame.font.Font(os.path.join(font_path, "stacker.ttf"), 30)
        self.font_comicsans_big = pygame.font.SysFont("comicsans", 40)
        self.font_comicsans_middle = pygame.font.SysFont("comicsans", 30)
        self.font_comicsans_small = pygame.font.SysFont("comicsans", 22)

    def load_config(self):
        with open('config.json', 'r') as file:
            self.config = json.load(file)

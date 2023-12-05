import pygame
from src.entity import Entity
from src.player import Player


class PowerUp(Entity):
    """
    Class representing power-up entities in the game.
    """
    def __init__(self, position, images, powerup_type):
        """
        Initializes a power-up with a given position, animation images, and type.

        Args:
            position (tuple): The initial position (x, y) of the power-up.
            images (list): List of images for power-up animation.
            powerup_type (PowerUpType): The type of power-up.
        """
        super().__init__(position, images, None)
        self.type = powerup_type

    def apply_powerup(self, player):
        """
        Applies the power-up effect to the player.

        Args:
            player (Player): The player to apply the power-up to.
        """
        pass

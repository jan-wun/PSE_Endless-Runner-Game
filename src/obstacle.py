import pygame
from src.entity import Entity


class Obstacle(Entity):
    """
    Class representing obstacles in the game.
    """
    def __init__(self, position, images, obstacle_type):
        """
        Initializes an obstacle with a given position, animation images, and type.

        Args:
            position (tuple): The initial position (x, y) of the obstacle.
            images (list): List of images for obstacle animation.
            obstacle_type (ObstacleType): The type of obstacle.
        """
        super().__init__(position, images, None)
        self.type = obstacle_type

    def collide(self, player):
        """
        Handles collision with the player.

        Args:
            player: The player entity.
        """
        # Implement obstacle collision logic, e.g., deduct health from the player
        pass

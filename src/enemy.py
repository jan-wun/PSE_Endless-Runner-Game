import pygame
from src.entity import Entity


class Enemy(Entity):
    """
    Class representing enemies in the game.
    """
    def __init__(self, position, images, enemy_type):
        """
        Initializes an enemy with a given position, animation images, and type.

        Args:
            position (tuple): The initial position (x, y) of the enemy.
            images (list): List of images for enemy animation.
            enemy_type (EnemyType): The type of enemy.
        """
        super().__init__(position, images, None)
        self.type = enemy_type

    def move(self):
        """
        Handles enemy movement logic.
        """
        pass

    def attack(self):
        """
        Handles enemy attack logic.
        """
        pass

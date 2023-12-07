import pygame
from src.entity import Entity


class Obstacle(Entity):
    """
    Class representing obstacles in the game.
    """
    def __init__(self, position, images, obstacle_type, speed, game):
        """
        Initializes an obstacle with a given position, animation images, and type.

        Args:
            position (tuple): The initial position (x, y) of the obstacle.
            images (list): List of images for obstacle animation.
            obstacle_type (ObstacleType): The type of obstacle.
            speed (int): The movement speed of the obstacle.
            game (object): Game object.
        """
        super().__init__(position, images, None)
        self.type = obstacle_type
        self.speed = speed
        self.game = game

    def move(self):
        self.position[0] -= (self.game.scrolling_bg_speed + self.speed)
        if self.position[0] <= 0 - self.image.get_width():
            self.position[0] = self.game.width + 200

    def collide(self, player):
        """
        Handles collision with the player.

        Args:
            player: The player entity.
        """
        # Implement obstacle collision logic, e.g., deduct health from the player
        pass

    def update(self):
        self.move()
        super().update()

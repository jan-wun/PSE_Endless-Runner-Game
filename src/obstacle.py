import pygame
from src.entity import Entity


class Obstacle(Entity):
    """
    Class representing obstacles in the game.
    """

    def __init__(self, position, images, obstacle_type, speed, game):
        """
        Initializes an obstacle with a given position, animation images, type and speed.

        Args:
            position (tuple): The initial position (x, y) of the obstacle.
            images (list): List of images for obstacle animation.
            obstacle_type (ObstacleType): The type of obstacle.
            speed (int): The movement speed of the obstacle.
            game (object): Game object.
        """
        super().__init__(position, images, None, game)
        self.type = obstacle_type
        self.speed = speed

    def move(self):
        """
        Handles the obstacle movement.
        """
        self.position[0] -= (self.game.scrolling_bg_speed + self.speed)
        # Kill obstacle if it moves out of screen.
        if self.position[0] <= 0 - self.image.get_width():
            self.kill()

    def update(self):
        """
        Updates obstacle.
        """
        self.move()
        super().update()

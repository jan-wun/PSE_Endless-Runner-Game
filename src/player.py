import pygame
from src.entity import Entity
from src.enums import PlayerState


class Player(Entity):
    """
    Class representing the player in the game.
    """
    def __init__(self, position, images_idle, images_walk, images_jump):
        """
        Initializes the player with a given position and animation images.

        Args:
            position (tuple): The initial position (x, y) of the player.
            images_idle (list): List of images for idle animation.
            images_walk (list): List of images for walking animation.
            images_jump (list): List of images for jumping animation.
        """
        super().__init__(position, images_idle, PlayerState.IDLE)
        # Set initial health.
        self.health = 1
        self.weapon = None
        self.images_idle = images_idle
        self.images_walk = images_walk
        self.images_jump = images_jump
        self.current_state = PlayerState.IDLE

    def move_left(self):
        """
        Move the player to the left.
        """
        pass

    def move_right(self):
        """
        Move the player to the right.
        """
        pass

    def jump(self):
        """
        Make the player jump.
        """
        pass

    def slide(self):
        """
        Make the player slide.
        """
        # Implement slide logic

    def shoot(self):
        """
        Make the player shoot (if a weapon is equipped).
        """
        pass

import pygame
from src.entity import Entity


class Weapon(Entity):
    """
    Class representing weapons in the game.
    """
    def __init__(self, position, images, weapon_type, damage):
        """
        Initializes a weapon with a given position, animation images, type, and damage.

        Args:
            position (tuple): The initial position (x, y) of the weapon.
            images (list): List of images for weapon animation.
            weapon_type (WeaponType): The type of weapon.
            damage (int): The damage inflicted by the weapon.
        """
        super().__init__(position, images, None)
        self.type = weapon_type
        self.damage = damage

    def fire(self):
        """
        Fires the weapon.
        """
        pass

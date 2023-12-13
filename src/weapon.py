import pygame
from src.entity import Entity
from src.enums import PlayerState


class Weapon(Entity):
    """
    Class representing weapons in the game.
    """
    def __init__(self, position, images, weapon_type, damage, game, player):
        """
        Initializes a weapon with a given position, animation images, type, and damage.

        Args:
            position (tuple): The initial position (x, y) of the weapon.
            images (list): List of images for weapon animation.
            weapon_type (WeaponType): The type of weapon.
            damage (int): The damage inflicted by the weapon.
        """
        super().__init__(position, images, None, game)
        self.type = weapon_type
        self.damage = damage
        self.player = player

    def fire(self):
        """
        Fires the weapon.
        """
        # Set the weapon's position based on the player's position.
        print("Feuer")

    def update(self):
        """
        Updates the weapon.
        """
        # Update weapon position based on current player movement and image.
        if self.player.current_state == PlayerState.WALKING_LEFT or self.player.current_state == PlayerState.IDLE and self.player.previous_walking_state == PlayerState.WALKING_LEFT:
            self.image = self.image_list[1]
            self.position = [self.player.position[0] - self.rect.width, self.player.position[1] + 30]
        elif self.player.current_state == PlayerState.WALKING_RIGHT or self.player.current_state == PlayerState.IDLE and self.player.previous_walking_state == PlayerState.WALKING_RIGHT:
            self.image = self.image_list[0]
            self.position = [self.player.position[0] + self.player.rect.width, self.player.position[1] + 30]
        elif self.player.current_state == PlayerState.JUMPING:
            if self.player.previous_walking_state == PlayerState.WALKING_LEFT:
                self.image = self.image_list[1]
                self.position = [self.player.position[0] - self.rect.width, self.player.position[1] + 30]
            else:
                self.image = self.image_list[0]
                self.position = [self.player.position[0] + self.player.rect.width, self.player.position[1] + 30]
        elif self.player.current_state == PlayerState.SLIDING:
            if self.player.previous_walking_state == PlayerState.WALKING_LEFT:
                self.image = self.image_list[1]
                self.position = [self.player.position[0] + self.player.rect.width - self.rect.width - 30,
                                 self.player.position[1] - self.rect.height]
            else:
                self.image = self.image_list[0]
                self.position = [self.player.position[0] + 30, self.player.position[1] - self.rect.height]

        super().update()

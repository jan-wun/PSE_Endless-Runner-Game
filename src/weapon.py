import pygame
from src.entity import Entity
from src.enums import PlayerState, WeaponType
from src.projectile import Projectile


class Weapon(Entity):
    """
    Class representing weapons in the game.
    """

    def __init__(self, position, weapon_type, game, player):
        """
        Initializes a weapon with a given position and type.

        Args:
            position (tuple): The initial position (x, y) of the weapon.
            weapon_type (WeaponType): The type of weapon.
            damage (int): The damage inflicted by the weapon.
        """
        self.type = weapon_type
        self.player = player
        if self.type == WeaponType.DEFAULT:
            self.projectile_image = pygame.transform.scale_by(
                pygame.image.load("assets/images/bullets/default_weapon.png").convert_alpha(), 3)
            self.shot_speed = 5
            self.shots = 1
            images = [pygame.transform.scale_by(
                pygame.image.load("assets/images/player/weapon/weapon1_right.png").convert_alpha(), 2.5),
                      pygame.transform.scale_by(
                          pygame.image.load("assets/images/player/weapon/weapon1_left.png").convert_alpha(), 2.5)]
        else:
            self.projectile_image = pygame.transform.scale_by(
                pygame.image.load("assets/images/bullets/upgrade_weapon.png").convert_alpha(), 3)
            self.shot_speed = 8
            self.shots = 2
            images = [pygame.transform.scale_by(
                pygame.image.load("assets/images/player/weapon/weapon2_right.png").convert_alpha(), 2.5),
                      pygame.transform.scale_by(
                          pygame.image.load("assets/images/player/weapon/weapon2_left.png").convert_alpha(), 2.5)]

        super().__init__(position, images, None, game)

    def fire(self):
        """
        Fires the weapon.
        """
        self.shots -= 1
        if self.image == self.image_list[0]:
            projectile_x_position = self.position[0] + self.rect.width
            projectile_velocity = [self.shot_speed, 0]
        else:
            projectile_x_position = self.position[0]
            projectile_velocity = [-(self.shot_speed + self.game.scrolling_bg_speed), 0]
        self.game.projectiles.add(
            Projectile([projectile_x_position, self.position[1] + 5], projectile_velocity,
                       [self.projectile_image], self.game, "player"))

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

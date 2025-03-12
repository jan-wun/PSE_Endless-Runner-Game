import pygame
from src.assets import Assets
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
            player (Player): The player of the game.
        """
        self.assets = Assets()
        self.type = weapon_type
        self.player = player

        # Default scaling
        self.scale_factor = 1.0

        # Set image, shot speed and number of shots based on weapon type.
        if self.type == WeaponType.DEFAULT:
            self.projectile_image = self.assets.default_weapon_bullet
            self.shot_speed = self.assets.config["shot_speed_default_weapon"]
            self.max_shots = self.assets.config["shots_default_weapon"]
            self.shots = self.max_shots
            images = self.assets.default_weapon_images
        else:
            self.projectile_image = self.assets.upgrade_weapon_bullet
            self.shot_speed = self.assets.config["shot_speed_upgrade_weapon"]
            self.max_shots = self.assets.config["shots_upgrade_weapon"]
            self.shots = self.max_shots
            images = self.assets.upgrade_weapon_images

        super().__init__(position, images, None, game)

        # Store original dimensions for scaling
        self.original_width = self.rect.width
        self.original_height = self.rect.height

    def fire(self):
        """
        Fires the weapon.
        """
        # Decrease shots.
        self.shots -= 1
        # Shot needs to move to the right, when weapon is directed to the right side and vice versa.
        if self.image == self.image_list[0]:
            projectile_x_position = self.position[0] + self.rect.width
            projectile_velocity = [self.shot_speed, 0]
        else:
            projectile_x_position = self.position[0]
            projectile_velocity = [-(self.shot_speed + self.game.scrolling_bg_speed), 0]
        # Add projectile to projectiles sprite group.
        self.game.projectiles.add(
            Projectile([projectile_x_position, self.position[1] + 5], projectile_velocity,
                       [self.projectile_image], self.game, "player"))

    def update(self):
        """
        Updates the weapon.
        """
        # Update weapon position based on current player movement and image.
        if self.player.current_state in [PlayerState.WALKING_LEFT,
                                         PlayerState.IDLE] and self.player.previous_walking_state == PlayerState.WALKING_LEFT:
            self.image = pygame.transform.scale(self.image_list[1], (
            int(self.original_width * self.scale_factor), int(self.original_height * self.scale_factor)))
            self.position = [self.player.position[0] - self.rect.width, self.player.position[1] + 30]
        elif self.player.current_state in [PlayerState.WALKING_RIGHT,
                                           PlayerState.IDLE] and self.player.previous_walking_state == PlayerState.WALKING_RIGHT:
            self.image = pygame.transform.scale(self.image_list[0], (
            int(self.original_width * self.scale_factor), int(self.original_height * self.scale_factor)))
            self.position = [self.player.position[0] + self.player.rect.width, self.player.position[1] + 30]
        elif self.player.current_state == PlayerState.JUMPING:
            if self.player.previous_walking_state == PlayerState.WALKING_LEFT:
                self.image = pygame.transform.scale(self.image_list[1], (
                int(self.original_width * self.scale_factor), int(self.original_height * self.scale_factor)))
                self.position = [self.player.position[0] - self.rect.width, self.player.position[1] + 30]
            else:
                self.image = pygame.transform.scale(self.image_list[0], (
                int(self.original_width * self.scale_factor), int(self.original_height * self.scale_factor)))
                self.position = [self.player.position[0] + self.player.rect.width, self.player.position[1] + 30]
        elif self.player.current_state == PlayerState.SLIDING:
            if self.player.previous_walking_state == PlayerState.WALKING_LEFT:
                self.image = pygame.transform.scale(self.image_list[1], (
                int(self.original_width * self.scale_factor), int(self.original_height * self.scale_factor)))
                self.position = [self.player.position[0] + self.player.rect.width - self.rect.width - 30,
                                 self.player.position[1] - self.rect.height]
            else:
                self.image = pygame.transform.scale(self.image_list[0], (
                int(self.original_width * self.scale_factor), int(self.original_height * self.scale_factor)))
                self.position = [self.player.position[0] + 30, self.player.position[1] - self.rect.height]

        # Update rect based on the new image size
        self.rect = self.image.get_rect(topleft=self.position)
        super().update()

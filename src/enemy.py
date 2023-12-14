import pygame
import random
from src.entity import Entity
from src.enums import EnemyType, EnemyState
from src.projectile import Projectile


class Enemy(Entity):
    """
    Class representing enemies in the game.
    """
    def __init__(self, position, enemy_type, game):
        """
        Initializes an enemy with a given position and type.

        Args:
            position (list): The initial position (x, y) of the enemy.
            enemy_type (EnemyType): The type of enemy.
        """
        self.type = enemy_type

        # Load enemy images based on type.
        if self.type == EnemyType.DRONE:
            self.image_list = [pygame.transform.scale_by(
                pygame.image.load(f"assets/images/enemies/drone/idle/idle{i}.png").convert_alpha(), 3) for i in
                               range(1, 5)]
            self.projectile_image = pygame.transform.scale_by(
                pygame.image.load(f"assets/images/bullets/capsule.png").convert_alpha(),
                1.5)

        else:
            self.image_list = [pygame.transform.scale_by(
                pygame.image.load(f"assets/images/enemies/robot/idle/idle{i}.png").convert_alpha(), 3) for i in
                               range(1, 5)]
            self.projectile_image = pygame.transform.scale_by(
                pygame.image.load(f"assets/images/bullets/projectile.png").convert_alpha(),
                1.5)
        super().__init__(position, self.image_list, EnemyState.IDLE, game)
        self.speed = 1 if self.type == EnemyType.ROBOT else 3
        self.attack_timer = 0

    def handle_movement(self):
        """
        Handles enemy movement logic.
        """
        if self.type == EnemyType.DRONE:
            if not self.current_state == EnemyState.WALKING_LEFT and self.position[0] < self.game.width - self.rect.width:
                self.move_right()
            else:
                if self.position[0] > 0:
                    self.move_left()
                else:
                    self.current_state = EnemyState.WALKING_RIGHT
        elif self.type == EnemyType.ROBOT:
            if self.position[0] > self.game.player.sprite.position[0]:
                self.move_left()
            elif self.position[0] < self.game.player.sprite.position[0]:
                self.move_right()

    def move_left(self):
        self.current_state = EnemyState.WALKING_LEFT
        self.position[0] -= (self.speed + self.game.scrolling_bg_speed)

    def move_right(self):
        self.current_state = EnemyState.WALKING_RIGHT
        self.position[0] += self.speed

    def attack(self):
        """
        Handles enemy attack logic.
        """
        self.attack_timer += 1
        if self.attack_timer % 60 == 0:
            if random.random() < 0.2:
                if self.type == EnemyType.DRONE:
                    projectile_position = [self.position[0] + self.rect.width / 2, self.position[1] + self.rect.height]
                    self.game.projectiles.add(Projectile(projectile_position, [0, 5], [self.projectile_image], self.game))
                elif self.type == EnemyType.ROBOT:
                    if self.game.player.sprite.position[0] < self.position[0]:
                        projectile_position = [self.position[0], self.position[1] + 40]
                        self.game.projectiles.add(Projectile(projectile_position, [-5 - self.game.scrolling_bg_speed, 0], [self.projectile_image], self.game))
                    else:
                        projectile_position = [self.position[0] + self.rect.width, self.position[1] + 40]
                        self.game.projectiles.add(Projectile(projectile_position, [5, 0], [self.projectile_image], self.game))

    def update(self):
        self.handle_movement()
        self.attack()
        super().update()

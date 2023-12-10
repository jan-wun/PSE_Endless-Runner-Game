import pygame
from src.entity import Entity
from src.enums import EnemyType


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
        else:
            self.image_list = [pygame.transform.scale_by(
                pygame.image.load(f"assets/images/enemies/robot/idle/idle{i}.png").convert_alpha(), 3) for i in
                               range(1, 5)]
        super().__init__(position, self.image_list, None, game)

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

    def update(self):
        self.move()
        super().update()

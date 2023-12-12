import pygame
from src.entity import Entity
from src.enums import EnemyType, EnemyState


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
        super().__init__(position, self.image_list, EnemyState.IDLE, game)
        self.speed = 1 if self.type == EnemyType.ROBOT else 3

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
            if self.position[0] > self.game.player.position[0]:
                self.move_left()
            elif self.position[0] < self.game.player.position[0]:
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
        pass


    def update(self):
        self.handle_movement()
        super().update()

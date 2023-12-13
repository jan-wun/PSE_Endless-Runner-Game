import pygame
from src.entity import Entity
from src.enums import EnemyType


class Projectile(Entity):
    def __init__(self, position, velocity, image_list, game):
        super().__init__(position, image_list, None, game)
        self.velocity = velocity

    def update(self):
        # Update the projectile's position
        self.position[0] += self.velocity[0]
        self.position[1] += self.velocity[1]

        # If the projectile goes out of the screen, remove it
        if not self.game.screen.get_rect().colliderect(self.rect):
            self.kill()

        super().update()

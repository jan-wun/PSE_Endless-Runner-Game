import pygame
from src.entity import Entity


class Projectile(Entity):
    def __init__(self, position, velocity, image_list, game, shooter):
        super().__init__(position, image_list, None, game)
        self.velocity = velocity
        self.shooter = shooter

    def update(self):
        # Update the projectile's position
        self.position[0] += self.velocity[0]
        self.position[1] += self.velocity[1]

        # If the projectile goes out of the screen, remove it
        if not self.game.screen.get_rect().colliderect(self.rect):
            if self.shooter == "player":
                self.game.player.sprite.weapon.shots += 1
            self.kill()

        super().update()

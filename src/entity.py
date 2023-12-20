import pygame
from src.enums import GameState


class Entity(pygame.sprite.Sprite):
    """
    Base class for game entities.
    """

    def __init__(self, position, image_list, current_state, game):
        """
        Initializes an entity with a given position, list of images, and current state.

        Args:
            position (list): The initial position (x, y) of the entity.
            image_list (list): List of images for animation.
            current_state: The current state of the entity.
            game (object): Game object.
        """
        super().__init__()
        self.position = position
        self.image_list = image_list
        self.current_state = current_state

        # The current image to be displayed.
        self.image = self.image_list[0]
        self.rect = self.image.get_rect()
        # Initial position of image.
        self.rect.topleft = (self.position[0], self.position[1])

        self.game = game

    def update(self):
        """
        Update logic that is the same for all entities.
        """
        # Update the position of the rect based on the entity's position.
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.position[0], self.position[1])

    def check_collision(self, group):
        """
        Checks for collision with sprite group.

        Args:
            group: The sprite group to check for collision with.
        """
        hit_sprite = pygame.sprite.spritecollideany(self, group)
        if hit_sprite:
            from src.enemy import Enemy
            from src.player import Player
            from src.powerup import PowerUp
            if isinstance(self, Enemy):
                hit_sprite.kill()
                self.kill()
            elif isinstance(self, Player):
                if isinstance(hit_sprite, PowerUp):
                    hit_sprite.kill()
                    hit_sprite.apply_powerup()
                else:
                    self.health -= 1
                    if self.health == 0:
                        self.game.current_state = GameState.GAME_OVER
                    else:
                        [obstacle.kill() for obstacle in self.game.obstacles]
                        [enemy.kill() for enemy in self.game.enemies]
                        [projectile.kill() for projectile in self.game.projectiles]

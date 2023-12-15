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
            if isinstance(self, Enemy):
                hit_sprite.kill()
                self.kill()
            else:
                self.game.current_state = GameState.GAME_OVER

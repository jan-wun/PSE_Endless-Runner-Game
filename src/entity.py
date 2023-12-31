import pygame


class Entity(pygame.sprite.Sprite):
    """
    Base class for game entities. Inherits from pygame.sprite.Sprite.
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
        self.game = game
        self.current_state = current_state

        # The current image to be displayed.
        self.image = self.image_list[0]
        self.rect = self.image.get_rect()
        # Initial position of the image.
        self.rect.topleft = (self.position[0], self.position[1])

    def update(self):
        """
        Update logic that is the same for all entities.
        """
        # Update the position of the rect based on the entity's position.
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.position[0], self.position[1])

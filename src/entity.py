import pygame


class Entity(pygame.sprite.Sprite):
    """
    Base class for game entities.
    """

    def __init__(self, position, image_list, current_state):
        """
        Initializes an entity with a given position, list of images, and current state.

        Args:
            position (tuple): The initial position (x, y) of the entity.
            image_list (list): List of images for animation.
            current_state: The current state of the entity.
        """
        super().__init__()
        self.position = position
        self.image_list = image_list
        self.current_state = current_state
        # The current image to be displayed.
        self.image = None

    def update(self):
        """
        Update logic that is the same for all entities.
        """
        pass

    def render(self, screen):
        """
        Renders the current image on the provided screen.

        Args:
            screen: The Pygame surface to render the image on.
        """
        pass

    def check_collision(self, other_entity):
        """
        Checks for collision with another entity.

        Args:
            other_entity: The entity to check for collision with.
        """
        pass

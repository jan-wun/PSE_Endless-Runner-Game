import pygame
from src.entity import Entity
from src.enums import PlayerState


class Player(Entity):
    """
    Class representing the player in the game.
    """
    def __init__(self, position, images_idle, images_walk, images_jump, images_slide):
        """
        Initializes the player with a given position and animation images.

        Args:
            position (list): The initial position [x, y] of the player.
            images_idle (list): List of images for idle animation.
            images_walk (list): List of images for walking animation.
            images_jump (list): List of images for jumping animation.
            images_slide (list): List of images for sliding animation.
        """
        super().__init__(position, images_idle, PlayerState.IDLE)
        # Set initial health.
        self.health = 1
        self.weapon = None
        self.images_idle = images_idle
        self.images_walk = images_walk
        self.images_jump = images_jump
        self.images_slide = images_slide

        # Movement parameters.
        self.speed = 5
        self.jump_height = 20
        self.jump_speed = self.jump_height
        self.is_jumping = False

        # Initialize player state.
        self.current_state = PlayerState.IDLE

    def handle_input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT]:
            self.move_right()
        elif keys[pygame.K_LEFT]:
            self.move_left()

        if keys[pygame.K_UP]:
            self.is_jumping = True
        elif keys[pygame.K_DOWN]:
            self.slide()

    def move_left(self):
        """
        Move the player to the left.
        """
        self.current_state = PlayerState.WALKING
        self.position[0] -= self.speed

    def move_right(self):
        """
        Move the player to the right.
        """
        self.current_state = PlayerState.WALKING
        self.position[0] += self.speed

    def jump(self):
        """
        Make the player jump.
        """
        if self.is_jumping:
            self.current_state = PlayerState.JUMPING

            # Check if the jump is still going.
            if self.jump_speed >= -self.jump_height:
                # Determine the direction of the jump.
                direction = 1 if self.jump_speed >= 0 else -1
                # Adjust the player's vertical position based on the jump speed.
                self.position[1] -= self.jump_speed ** 2 * 0.1 * direction
                # Decrease the jump speed.
                self.jump_speed -= 1
            else:
                # Reset jumping state and jump speed.
                self.is_jumping = False
                self.jump_speed = self.jump_height

    def slide(self):
        """
        Make the player slide.
        """
        # Implement slide logic
        pass

    def shoot(self):
        """
        Make the player shoot (if a weapon is equipped).
        """
        pass

    def update(self):
        super().update()
        self.handle_input()
        self.jump()

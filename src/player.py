import pygame
from src.assets import Assets
from src.entity import Entity
from src.enums import PlayerState, WeaponType, GameState
from src.weapon import Weapon


class Player(Entity):
    """
    Class representing the player in the game.
    """
    def __init__(self, images_idle, images_walk, images_jump, images_slide, game):
        """
        Initializes the player with a given position and animation images.

        Args:
            images_idle (list): List of images for idle animation.
            images_walk (list): List of images for walking animation.
            images_jump (list): List of images for jumping animation.
            images_slide (list): List of images for sliding animation.
            game (object): Game object.
        """
        self.assets = Assets()
        # Initial position of the player.
        self.position = [100, 520]

        super().__init__(self.position, images_idle, PlayerState.IDLE, game)
        # Set initial health.
        self.health = 1

        self.invincible = False
        self.invincible_time = self.game.fps * 5

        # Create default weapon for the player.
        self.weapon = Weapon([self.position[0] + self.rect.width, self.position[1] + 30], WeaponType.DEFAULT, game, self)

        # Set images for player movement animations.
        self.images_idle = images_idle
        self.images_walk = images_walk
        self.images_jump = images_jump
        self.images_slide = images_slide

        # Movement parameters.
        self.speed = 5
        self.jump_height = 20
        self.jump_speed = self.jump_height
        self.is_jumping = False
        self.is_sliding = False
        self.slide_height = 600
        self.slide_speed_reduction = 0.1
        self.slide_end_position = 80
        self.slide_speed = self.speed
        self.shoot_pressed = True
        # Cooldown parameters for sliding.
        self.slide_cooldown = 0
        self.slide_cooldown_max = 150

        # Initialize animation-related variables.
        self.animation_speed = 6
        self.current_frame = 0

        # Initialize player state.
        self.current_state = PlayerState.IDLE
        self.previous_walking_state = PlayerState.IDLE

        # Create a dictionary to map player states to animation sequences.
        self.animations = {
            PlayerState.IDLE: self.images_idle,
            PlayerState.WALKING_LEFT: self.images_walk,
            PlayerState.WALKING_RIGHT: self.images_walk,
            PlayerState.JUMPING: self.images_jump,
            PlayerState.SLIDING: self.images_slide
        }

    def handle_input(self):
        keys = pygame.key.get_pressed()

        if self.game.current_state == GameState.PLAYING:
            # Handle horizontal movement input.
            if keys[pygame.K_RIGHT] and not keys[pygame.K_LEFT] and not self.is_sliding:
                self.move_right()
            elif keys[pygame.K_LEFT] and not keys[pygame.K_RIGHT] and not self.is_sliding:
                self.move_left()
            else:
                self.current_state = PlayerState.IDLE

            # Handle jump and slide input.
            if keys[pygame.K_UP]:
                if not self.is_jumping and not self.is_sliding:
                    self.assets.sounds["jump"].play()
                    self.is_jumping = True
            elif keys[pygame.K_DOWN]:
                if (keys[pygame.K_LEFT] or keys[pygame.K_RIGHT]) and not self.is_jumping and not self.is_sliding and \
                        self.slide_cooldown == 0:
                    self.is_sliding = True
                    self.slide_cooldown = self.slide_cooldown_max

            # Handle shooting input.
            if keys[pygame.K_SPACE] and not self.shoot_pressed:
                self.shoot()
                self.shoot_pressed = True
            elif not keys[pygame.K_SPACE]:
                self.shoot_pressed = False

    def move_left(self):
        """
        Move the player to the left.
        """
        self.current_state = PlayerState.WALKING_LEFT
        # Make sure that the new position is within the left boundary.
        new_x = self.position[0] - (self.speed + self.game.scrolling_bg_speed)
        self.position[0] = max(new_x, 0)

    def move_right(self):
        """
        Move the player to the right.
        """
        self.current_state = PlayerState.WALKING_RIGHT
        # Make sure that the new position is within the right boundary.
        new_x = self.position[0] + self.speed
        self.position[0] = min(new_x, self.game.width - self.rect.width)

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

                # Check for simultaneous key presses during the jump.
                keys = pygame.key.get_pressed()
                if keys[pygame.K_LEFT]:
                    self.previous_walking_state = PlayerState.WALKING_LEFT
                elif keys[pygame.K_RIGHT]:
                    self.previous_walking_state = PlayerState.WALKING_RIGHT
            else:
                # Reset jumping state and jump speed.
                self.is_jumping = False
                self.jump_speed = self.jump_height

    def slide(self):
        """
        Make the player slide.
        """
        if self.is_sliding:
            self.current_state = PlayerState.SLIDING
            self.position[1] = self.slide_height

            # Gradually reduce speed during the slide.
            self.slide_speed -= self.slide_speed_reduction

            if self.slide_speed > 0:
                # Calculate new x position of player when he slides to the right.
                if self.previous_walking_state == PlayerState.WALKING_RIGHT:
                    new_x = self.position[0] + self.slide_speed
                # Calculate new x position of player when he slides to the left.
                elif self.previous_walking_state == PlayerState.WALKING_LEFT:
                    new_x = self.position[0] - (self.slide_speed + self.game.scrolling_bg_speed)

                # Make sure that the new x position is within the boundaries.
                new_x = max(0, min(new_x, self.game.width - self.rect.width))
                # Move player to new x position.
                self.position[0] = new_x
            else:
                # End sliding when the speed is zero.
                self.is_sliding = False
                self.position[1] -= self.slide_end_position
                if self.previous_walking_state == PlayerState.WALKING_RIGHT:
                    self.position[0] += self.image.get_width() - self.images_idle[0].get_width()
                # Reset speed to the default value.
                self.slide_speed = self.speed

    def update_animation(self):
        """
        Update the animation based on the current player state.
        """
        self.image_list = self.animations.get(self.current_state)
        # Check if the player is moving to the left or was moving to the left before jumping / sliding.
        moving_left = self.current_state == PlayerState.WALKING_LEFT
        moving_left_jump = self.current_state == PlayerState.JUMPING and \
                                  self.previous_walking_state == PlayerState.WALKING_LEFT
        moving_left_slide = (self.current_state == PlayerState.SLIDING or
                                    self.current_state == PlayerState.IDLE) and \
                                   self.previous_walking_state == PlayerState.WALKING_LEFT
        if moving_left or moving_left_jump or moving_left_slide:
            # Flip images vertically.
            self.image_list = [pygame.transform.flip(image, True, False) for image in self.image_list]
        self.image = self.image_list[0]

        # Update the animation frame.
        self.update_animation_frame()

    def update_animation_frame(self):
        """
        Update the animation frame based on the elapsed time.
        """
        # Calculate the index of the current frame based on the current frame counter and animation speed.
        self.current_frame = (self.current_frame + self.animation_speed/100) % len(self.image_list)

        # Set the image of the sprite to the one corresponding to the calculated index.
        self.image = self.image_list[int(self.current_frame)]

    def shoot(self):
        """
        Make the player shoot (if a weapon is equipped).
        """
        if self.weapon is not None and self.weapon.shots >= 1:
            self.weapon.fire()
            self.assets.sounds['shoot'].play()

    def update(self):
        self.handle_input()
        self.jump()
        self.slide()
        if self.slide_cooldown > 0:
            self.slide_cooldown -= 1
        if self.invincible:
            if self.invincible_time > 0:
                self.invincible_time -= 1
            else:
                self.invincible = False
        self.update_animation()
        # Set the previous walking state at the end of the update method.
        if self.current_state == PlayerState.WALKING_LEFT or self.current_state == PlayerState.WALKING_RIGHT:
            self.previous_walking_state = self.current_state
        # Update weapon.
        self.weapon.update()
        super().update()

    def reset(self):
        """
        Resets player (position, animation, state, ...) which is necessary for restarting the game.
        """
        self.__init__(self.images_idle, self.images_walk, self.images_jump, self.images_slide, self.game)

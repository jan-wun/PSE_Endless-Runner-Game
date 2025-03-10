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
        Initializes the player with animation images.

        Args:
            images_idle (list): List of images for idle animation.
            images_walk (list): List of images for walking animation.
            images_jump (list): List of images for jumping animation.
            images_slide (list): List of images for sliding animation.
            game (Game): Game object.
        """
        self.assets = Assets()
        # Initial position of the player.
        self.position = [100, 520]

        super().__init__(self.position, images_idle, PlayerState.IDLE, game)

        # Set initial health.
        self.health = self.assets.config["initial_player_health"]

        self.invincible = False
        self.invincible_time = self.game.fps * self.assets.config["invincible_time"]

        # Create default weapon for the player.
        self.weapon = Weapon([self.position[0] + self.rect.width, self.position[1] + 30], WeaponType.DEFAULT, game,
                             self)

        # Set images for player movement animations.
        self.images_idle = images_idle
        self.images_walk = images_walk
        self.images_jump = images_jump
        self.images_slide = images_slide

        # Movement parameters.
        self.speed = self.assets.config["player_speed"]
        self.jump_height = self.assets.config["player_jump_height"]
        self.jump_speed = self.jump_height
        self.is_jumping = False
        self.is_sliding = False
        self.slide_height = self.assets.config["player_slide_height"]
        self.slide_speed_reduction = self.assets.config["player_slide_speed_reduction"]
        self.slide_end_position = self.assets.config["player_slide_end_position"]
        self.slide_speed = self.speed
        self.shoot_pressed = True
        # Cooldown parameters for sliding.
        self.slide_cooldown = 0
        self.slide_cooldown_max = self.assets.config["player_slide_cooldown_max"]

        # Initialize animation-related variables.
        self.animation_speed = self.assets.config["player_animation_speed"]
        self.current_frame = 0

        # Initialize player state.
        self.current_state = PlayerState.IDLE
        self.previous_walking_state = None

        # Create a dictionary to map player states to animation sequences.
        self.animations = {
            PlayerState.IDLE: self.images_idle,
            PlayerState.WALKING_LEFT: self.images_walk,
            PlayerState.WALKING_RIGHT: self.images_walk,
            PlayerState.JUMPING: self.images_jump,
            PlayerState.SLIDING: self.images_slide
        }

    def handle_input(self):
        """
        Handles input for player. Executes specific movement / action according to user input.
        """
        # Get pressed keys.
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
                        self.previous_walking_state and self.slide_cooldown == 0:
                    self.is_sliding = True
                    self.slide_cooldown = self.slide_cooldown_max

            # Handle shooting input.
            if keys[pygame.K_SPACE] and not self.shoot_pressed:
                self.shoot()
                self.shoot_pressed = True
            elif not keys[pygame.K_SPACE]:
                self.shoot_pressed = False

    ACTIONS = {
        "left": {
            "state": PlayerState.WALKING_LEFT,
            "position_update": lambda self: setattr(self, 'position', [max(self.position[0] - (self.speed + self.game.scrolling_bg_speed), 0), self.position[1]])
        },
        "right": {
            "state": PlayerState.WALKING_RIGHT,
            "position_update": lambda self: setattr(self, 'position', [min(self.position[0] + self.speed, self.game.width - self.rect.width), self.position[1]])
        },
        "jump": {
            "state": PlayerState.JUMPING,
            "condition": lambda self: self.is_jumping,
            "position_update": lambda self: (
                setattr(self, 'position', [self.position[0], self.position[1] - self.jump_speed ** 2 * 0.1 * (1 if self.jump_speed >= 0 else -1)]),
                setattr(self, 'jump_speed', self.jump_speed - 1),
                setattr(self, 'is_jumping', False) if self.jump_speed < -self.jump_height else None,
                setattr(self, 'jump_speed', self.jump_height) if not self.is_jumping else None,
                self.adjust_jump_direction()
            )
        },
        "slide": {
            "state": PlayerState.SLIDING,
            "condition": lambda self: self.is_sliding,
            "position_update": lambda self: (
                setattr(self, 'position', [self.position[0], self.slide_height]),
                setattr(self, 'slide_speed', self.slide_speed - self.slide_speed_reduction),
                setattr(self, 'position', [
                    max(0, min(
                        self.position[0] + self.slide_speed if self.previous_walking_state == PlayerState.WALKING_RIGHT else self.position[0] - (self.slide_speed + self.game.scrolling_bg_speed),
                        self.game.width - self.rect.width
                    )),
                    self.position[1]
                ]) if self.slide_speed > 0 else (
                    setattr(self, 'is_sliding', False),
                    setattr(self, 'position', [self.position[0], self.position[1] - self.slide_end_position]),
                    setattr(self, 'position', [self.position[0] + self.image.get_width() - self.images_idle[0].get_width(), self.position[1]]) if self.previous_walking_state == PlayerState.WALKING_RIGHT else None,
                    setattr(self, 'slide_speed', self.speed)
                )
            )
        }
    }

    def adjust_jump_direction(self):
        """
        Adjust the direction of the jump based on user input.
        """
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.previous_walking_state = PlayerState.WALKING_LEFT
        elif keys[pygame.K_RIGHT]:
            self.previous_walking_state = PlayerState.WALKING_RIGHT

    def perform_action(self, action):
        """
        Perform an action ("left", "right", "jump", "slide") using a dictionary-based approach.
        """
        if action in self.ACTIONS:
            action_data = self.ACTIONS[action]
            if "condition" not in action_data or action_data["condition"](self):
                self.current_state = action_data["state"]
                if "position_update" in action_data:
                    action_data["position_update"](self)


    def move_left(self):
        """
        Move the player to the left.
        """
        self.perform_action("left")

    def move_right(self):
        """
        Move the player to the right.
        """
        self.perform_action("right")

    def jump(self):
        """
        Make the player jump.
        """
        self.perform_action("jump")

    def slide(self):
        """
        Make the player slide.
        """
        self.perform_action("slide")

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
        self.current_frame = (self.current_frame + self.animation_speed / 100) % len(self.image_list)

        # Set the image of the sprite to the one corresponding to the calculated index.
        self.image = self.image_list[int(self.current_frame)]

    def shoot(self):
        """
        Make the player shoot (if a weapon is equipped, and he has shots left).
        """
        if self.weapon is not None and self.weapon.shots >= 1:
            self.weapon.fire()
            # Play shooting sound.
            self.assets.sounds['shoot'].play()

    def update(self):
        """
        Updates player.
        """
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
                self.invincible_time = self.game.fps * self.assets.config["invincible_time"]
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

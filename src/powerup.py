from src.entity import Entity
from src.enums import PowerUpType
from src.assets import Assets


class PowerUp(Entity):
    """
    Class representing power-up entities in the game.
    """

    def __init__(self, position, powerup_type, game):
        """
        Initializes a power-up with a given position, and type.

        Args:
            position (list): The initial position [x, y] of the power-up.
            powerup_type (PowerUpType): The type of power-up.
        """
        self.assets = Assets()
        self.type = powerup_type
        self.fall_speed = self.assets.config["power_up_fall_speed"]
        # Set image based on PowerUpType.
        if self.type == PowerUpType.INVINCIBILITY:
            images = self.assets.invincible_powerup
        elif self.type == PowerUpType.FREEZE:
            images = self.assets.freeze_powerup
        elif self.type == PowerUpType.MULTIPLE_SHOTS:
            images = self.assets.multiple_shots_power_up
        super().__init__(position, images, None, game)

    def apply_powerup(self):
        """
        Applies the power-up effect to the player.
        """
        if self.type == PowerUpType.INVINCIBILITY:
            self.game.player.sprite.invincible = True
        elif self.type == PowerUpType.FREEZE:
            self.game.freeze = True
        elif self.type == PowerUpType.MULTIPLE_SHOTS:
            self.game.player.sprite.weapon.max_shots = self.assets.config["multiple_shots"]
            self.game.player.sprite.weapon.shots = self.assets.config["multiple_shots"]

    def move(self):
        """
        Moves the power up down (fall speed) and to the left (scrolling background speed).
        """
        self.position[0] -= self.game.scrolling_bg_speed
        if self.position[1] <= self.game.height - 170:
            self.position[1] += self.fall_speed
        # Kill the power up if it moves out of screen.
        if self.position[0] <= 0 - self.image.get_width():
            self.kill()

    def update(self):
        """
        Update the power up.
        """
        self.move()
        super().update()

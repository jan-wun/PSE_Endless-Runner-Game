from src.entity import Entity


class Projectile(Entity):
    """
    Class representing projectiles.
    """

    def __init__(self, position, velocity, image_list, game, shooter):
        """
        Initializes a power-up with a given position, velocity, image and shooter.

        Args:
            position (list): The initial position [x, y] of the power-up.
            velocity (int): The velocity of the projectile.
            image_list (list): A list of the projectile images.
            shooter (str): The name of the shooter object (player, enemy).
        """
        super().__init__(position, image_list, None, game)
        self.velocity = velocity
        self.shooter = shooter

    def update(self):
        """
        Update the projectile.
        :return:
        """
        self.position[0] += self.velocity[0]
        self.position[1] += self.velocity[1]

        # If the projectile goes out of the screen, remove it and give player a shot back when he was the shooter.
        if not self.game.screen.get_rect().colliderect(self.rect):
            if self.shooter == "player":
                self.game.player.sprite.weapon.shots += 1
            self.kill()

        super().update()

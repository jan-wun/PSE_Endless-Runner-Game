import pygame
import sys
import random
from src.enums import GameState, EnemyType
from src.menu import Menu, GameOverMenu
from src.manager import AudioManager, ScoreManager
from src.player import Player
from src.obstacle import Obstacle
from src.enemy import Enemy


class Game:
    """
    The main class representing the endless runner game.
    """
    def __init__(self):
        """
        Initializes the Game object.

        This method sets up the Pygame environment, display, background image,
        entities, game state, distance, highscore, menu, audio manager, and score manager.
        """
        # Initialize Pygame.
        pygame.init()

        # Set up the display.
        self.width = 1344
        self.height = 768
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Run the Cybernetic City: Endless Dash")
        self.fps = 70

        # Load background image.
        self.background = pygame.image.load("assets/images/background.png").convert_alpha()

        # Initialize background position and scrolling speed.
        self.background_x = 0
        self.scrolling_bg_speed = 4

        # Initialize entities (player, enemies, powerups, obstacles, weapon).
        player_idle = [pygame.transform.scale_by(
            pygame.image.load(f"assets/images/player/idle/idle{i}.png").convert_alpha(), 4) for i in range(1, 5)]
        player_walk = [pygame.transform.scale_by(
            pygame.image.load(f"assets/images/player/walk/walk{i}.png").convert_alpha(), 4) for i in range(1, 7)]
        player_jump = [pygame.transform.scale_by(
            pygame.image.load(f"assets/images/player/jump/jump{i}.png").convert_alpha(), 4) for i in range(1, 5)]
        player_slide = [pygame.transform.scale_by(
            pygame.image.load(f"assets/images/player/slide/slide{i}.png").convert_alpha(), 4) for i in range(1, 2)]

        # Create obstacle objects.
        self.car_images = [
            pygame.transform.scale_by(pygame.image.load(f"assets/images/obstacles/car.png").convert_alpha(), 1.5)]
        self.meteor_images = [
            pygame.transform.scale_by(pygame.image.load(f"assets/images/obstacles/meteor.png").convert_alpha(), 0.25)]

        # Add timer for obstacle objects.
        self.obstacle_timer = pygame.USEREVENT + 1
        pygame.time.set_timer(self.obstacle_timer, 2000)

        # Add timer for enemy objects.
        self.enemy_timer = pygame.USEREVENT + 2
        pygame.time.set_timer(self.enemy_timer, 5000)

        # Create sprite group for obstacles.
        self.obstacles = pygame.sprite.Group()

        # Create sprite group for enemies.
        self.enemies = pygame.sprite.Group()

        # Create sprite group single for player.
        self.player = pygame.sprite.GroupSingle()
        self.player.add(Player(player_idle, player_walk, player_jump, player_slide, self))

        # Create sprite group for projectiles.
        self.projectiles = pygame.sprite.Group()

        # Initialize game state.
        self.current_state = GameState.PLAYING

        # Initialize distance and highscore.
        self.distance = 0
        with open("data.txt", "r") as file:
            self.highscore = int((file.readline().split("=")[1]))

        # Initialize menu, audio, and score manager.
        self.menu = Menu()
        self.game_over_screen = GameOverMenu()
        self.audio_manager = AudioManager()
        self.score_manager = ScoreManager()

    def start_game(self):
        """
        Starts the main game loop.
        """
        # Create a clock object to control the frame rate.
        clock = pygame.time.Clock()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    self.end_game()

                if self.current_state == GameState.PLAYING and event.type == self.obstacle_timer:
                    self.obstacles.add(random.choice([Obstacle([self.width + random.randint(200, 500), 480],
                                                              [pygame.transform.flip(image, True, False) for image in
                                                               self.car_images], 'car', 5, self),
                                                     Obstacle([self.width + random.randint(200, 500), 585],
                                                              self.meteor_images, 'meteor', 0,
                                                              self)]))
                if self.current_state == GameState.PLAYING and event.type == self.enemy_timer:
                    enemy_choice = random.choice([EnemyType.DRONE, EnemyType.ROBOT])
                    if not any(enemy.type == enemy_choice for enemy in self.enemies):
                        enemy_position = [400, 100] if enemy_choice == EnemyType.DRONE else [800, 512]
                        self.enemies.add(Enemy(enemy_position, enemy_choice, self))

                if self.current_state == GameState.GAME_OVER and event.type == pygame.KEYDOWN and \
                        event.key == pygame.K_SPACE:
                    self.restart_game()

            if self.current_state == GameState.PLAYING:
                # Update player.
                self.player.update()
                # Update all obstacles in the sprite group.
                self.obstacles.update()
                # Update all enemies in the sprite group.
                self.enemies.update()
                # Update all projectiles.
                self.projectiles.update()
                # Check for collision between player and obstacles.
                self.player.sprite.check_collision(self.obstacles)
                # Check for collision between player and enemies.
                self.player.sprite.check_collision(self.enemies)
                # Check for collision between player and projectiles.
                self.player.sprite.check_collision(self.projectiles)

                # Functionality for scrolling background.
                self.background_x -= self.scrolling_bg_speed
                # Check if the background has scrolled off the screen and reset position.
                if self.background_x <= -self.width:
                    self.background_x = 0

                # Update distance.
                self.distance += self.scrolling_bg_speed

                # Render game objects to the screen.
                self.render()

            elif self.current_state == GameState.GAME_OVER:
                # Update highscore if necessary.
                if self.distance > self.highscore:
                    self.highscore = self.distance
                    with open("data.txt", "w") as file:
                        file.write(f"highscore={self.highscore}")
                # Show game over screen.
                self.game_over_screen.show(self.screen, self.distance, self.highscore)

            # Cap the frame rate to defined fps.
            clock.tick(self.fps)

    def render(self):
        """
        Renders all game objects to the screen.
        """
        # Draw the background image with scroll position.
        self.screen.blit(self.background, (self.background_x, 0))
        # Create seamless scrolling effect.
        self.screen.blit(self.background, (self.background_x + self.width, 0))

        # Display current score on screen.
        distance_surface = pygame.font.SysFont("comicsansms", 40).render(f"Score: {self.distance}", True, (0, 255, 0))
        self.screen.blit(distance_surface, (10, 10))

        # Draw player.
        self.player.draw(self.screen)
        # Draw all obstacles in the sprite group.
        self.obstacles.draw(self.screen)
        # Draw all enemies in the sprite group.
        self.enemies.draw(self.screen)

        # Show border around player and enemies for debugging purpose only.
        pygame.draw.rect(self.screen, (255, 0, 0), self.player.sprite.rect, 2)
        for enemy in self.enemies:
            pygame.draw.rect(self.screen, (255, 0, 0), enemy.rect, 2)

        # Draw weapon.
        self.screen.blit(self.player.sprite.weapon.image, self.player.sprite.weapon.position)

        # Draw projectiles.
        self.projectiles.draw(self.screen)

        # Update the full display Surface to the screen.
        pygame.display.flip()

    def pause_game(self):
        """
        Pauses the game.
        """
        pass

    def end_game(self):
        """
        Ends the game.
        """
        pygame.quit()
        sys.exit()

    def restart_game(self):
        """
        Restarts the game.
        """
        # Kill all obstacles, enemies and projectiles.
        [obstacle.kill() for obstacle in self.obstacles]
        [enemy.kill() for enemy in self.enemies]
        [projectile.kill() for projectile in self.projectiles]

        # Reset the player.
        self.player.sprite.reset()

        # Reset travelled distance.
        self.distance = 0

        # Set current game state back to playing.
        self.current_state = GameState.PLAYING

    def show_settings_menu(self):
        """
        Displays the settings menu.
        """
        pass

    def show_power_ups_menu(self):
        """
        Displays the power-ups menu.
        """
        pass

    def show_statistics_menu(self):
        """
        Displays the statistics menu.
        """
        pass

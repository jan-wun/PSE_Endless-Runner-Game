import pygame
import sys
import random
from src.enums import GameState
from src.menu import Menu, GameOverMenu
from src.manager import AudioManager, ScoreManager
from src.player import Player
from src.obstacle import Obstacle


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

        # Create player object.
        self.player = Player(player_idle, player_walk, player_jump, player_slide, self)

        # Create obstacle objects.
        self.car_images = [
            pygame.transform.scale_by(pygame.image.load(f"assets/images/obstacles/car.png").convert_alpha(), 1.5)]
        self.meteor_images = [
            pygame.transform.scale_by(pygame.image.load(f"assets/images/obstacles/meteor.png").convert_alpha(), 0.5)]

        # Add timer for obstacle objects.
        self.obstacle_timer = pygame.USEREVENT + 1
        pygame.time.set_timer(self.obstacle_timer, 2000)

        # Create sprite group for entities (player and obstacles).
        self.entities = pygame.sprite.Group()

        # Add entities to the sprite group.
        self.entities.add(self.player)

        # Initialize game state.
        self.current_state = GameState.PLAYING

        # Initialize distance and highscore.
        self.distance = 0
        self.highscore = 0

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
                    pygame.quit()
                    sys.exit()

                if self.current_state == GameState.PLAYING and event.type == self.obstacle_timer:
                    self.entities.add(random.choice([Obstacle([self.width + random.randint(200, 500), 500],
                                                              [pygame.transform.flip(image, True, False) for image in
                                                               self.car_images], 'car', 5, self),
                                                     Obstacle([self.width + random.randint(200, 500), 515],
                                                              self.meteor_images, 'meteor', 0,
                                                              self)]))

                if self.current_state == GameState.GAME_OVER and event.type == pygame.KEYDOWN and \
                        event.key == pygame.K_SPACE:
                    self.restart_game()

            if self.current_state == GameState.PLAYING:
                # Update all entities in the sprite group.
                self.entities.update()
                # Check for collision between player and obstacles.
                self.entities.sprites()[0].check_collision(self.entities.sprites()[1:])

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
                # Show game over screen.
                self.game_over_screen.show(self.screen)

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

        # Draw all entities in the sprite group.
        self.entities.draw(self.screen)

        # Show border around entities for debugging purpose only.
        for entity in self.entities:
            pygame.draw.rect(self.screen, (255, 0, 0), entity.rect, 2)

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
        pass

    def restart_game(self):
        """
        Restarts the game.
        """
        # Kill all obstacles.
        for obstacle in self.entities.sprites()[1:]:
            obstacle.kill()

        # Reset the player.
        self.player.reset()

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

import pygame
import sys
from src.enums import GameState
from src.menu import Menu
from src.manager import AudioManager, ScoreManager


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
        self.fps = 60

        # Load background image.
        self.background = pygame.image.load("assets/images/background.png")

        # Initialize background position.
        self.background_x = 0

        # Initialize entities (player, enemies, powerups, obstacles, weapon).
        self.entities = [...]

        # Initialize game state.
        self.current_state = GameState.PLAYING

        # Initialize distance and highscore.
        self.distance = 0
        self.highscore = 0

        # Initialize menu, audio, and score manager.
        self.menu = Menu()
        self.audio_manager = AudioManager()
        self.score_manager = ScoreManager()

    def start_game(self):
        """
        Starts the main game loop.
        """
        # Create a clock object to control the frame rate.
        clock = pygame.time.Clock()

        while self.current_state == GameState.PLAYING:
            # Handle events (e.q., quitting the game).
            for event in pygame.event.get():
                if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

            # Functionality for scrolling background.
            if self.current_state == GameState.PLAYING:
                self.background_x -= 4
                # Check if the background has scrolled off the screen and reset position.
                if self.background_x <= -self.width:
                    self.background_x = 0

            # Render game objects to the screen.
            self.render()

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
        pass

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

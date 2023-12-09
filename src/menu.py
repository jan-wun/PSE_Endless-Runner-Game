import pygame


class Menu:
    """
    Represents the main menu in the game.
    """
    def display(self):
        """
        Displays the menu on the screen.
        """
        pass

    def handle_input(self):
        """
        Handles user input for the menu.
        """
        pass


class GameOverMenu:
    """
    Represents the game over screen.
    """
    def __init__(self):
        # Load game over image.
        self.image = pygame.transform.scale_by(pygame.image.load("assets/images/game_over.png").convert_alpha(), 0.5)

    def show(self, screen):
        # Fill background with black.
        screen.fill((0, 0, 0))

        # Draw game over image on screen.
        screen.blit(self.image, ((screen.get_width() - self.image.get_width()) / 2,
                                 (screen.get_height() - self.image.get_height()) / 2))
        # Message for restarting game.
        font = pygame.font.SysFont("comicsansms", 72)
        text_surface = font.render("Press space to run!", True, (0, 0, 128))
        screen.blit(text_surface, ((screen.get_width() - text_surface.get_width()) / 2, 500))

        # Update display.
        pygame.display.flip()

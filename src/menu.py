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

    def show(self, screen, distance, highscore):
        # Fill background with black.
        screen.fill((0, 0, 0))

        # Draw game over image on screen.
        screen.blit(self.image, ((screen.get_width() - self.image.get_width()) / 2,
                                 (screen.get_height() - self.image.get_height()) / 2))
        # Font for texts.
        font = pygame.font.SysFont("comicsansms", 72)

        # Text for travelled score.
        score_surface = font.render(f"Reached Score: {distance}", True, (0, 0, 255))
        screen.blit(score_surface, ((screen.get_width() - score_surface.get_width()) / 2, 80))

        # Text for highscore.
        highscore_surface = font.render(f"Highscore: {highscore}", True, (0, 0, 255))
        screen.blit(highscore_surface, ((screen.get_width() - highscore_surface.get_width()) / 2, 180))

        # Text for restarting game.
        text_surface = font.render("Press space to run!", True, (0, 0, 255))
        screen.blit(text_surface, ((screen.get_width() - text_surface.get_width()) / 2, 500))

        # Update display.
        pygame.display.flip()


class PauseMenu:
    """
    Represents the pause screen.
    """
    def __init__(self):
        # Load background image for pause screen.
        self.image = pygame.transform.scale_by(pygame.image.load("assets/images/pause.png").convert_alpha(), 0.15)
        self.rect = self.image.get_rect()

        # Font for texts.
        self.font_large = pygame.font.SysFont("comicsansms", 65)
        self.font_small = pygame.font.SysFont("comicsansms", 50)

    def handle_input(self, screen):
        """
        Handles user input for the pause menu.

        Returns:
            str: The action based on the button clicked ('resume', 'main_menu', 'quit').
        """
        # Draw background image on screen.
        self.rect.topleft = ((screen.get_width() - self.image.get_width()) / 2, (screen.get_height() - self.image.get_height()) / 2)
        screen.blit(self.image, self.rect.topleft)

        # Paused text.
        paused = self.font_large.render("PAUSED", True, (0, 255, 255))
        screen.blit(paused, (self.rect.centerx - paused.get_width() / 2, self.rect.top))

        # Button for resuming game.
        resume_button_rect = self.draw_button(screen, self.font_small, "RESUME", (0, 255, 0), (self.rect.centerx, 275))

        # Button for returning to the main menu.
        main_menu_button_rect = self.draw_button(screen, self.font_small, "MAIN MENU", (0, 0, 255), (self.rect.centerx, 375))

        # Button for quitting the game.
        quit_button_rect = self.draw_button(screen, self.font_small, "QUIT", (255, 0, 0), (self.rect.centerx, 475))

        # Check for mouse clicks.
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if pygame.mouse.get_pressed()[0]:  # 0 represents the left mouse button
            if resume_button_rect.collidepoint(mouse_x, mouse_y):
                return "resume"
            elif main_menu_button_rect.collidepoint(mouse_x, mouse_y):
                return "main_menu"
            elif quit_button_rect.collidepoint(mouse_x, mouse_y):
                return "quit"

        # Update display.
        pygame.display.flip()

    def draw_button(self, screen, font, text, color, position):
        """
        Draw a button on the screen.

        Args:
            screen (pygame.Surface): The screen to draw on.
            font (pygame.font.Font): The font for the button text.
            text (str): The text to display on the button.
            color (tuple): The color of the button.
            position (tuple): The position of the button's center.

        Returns:
            pygame.Rect: The rectangle representing the button's position and size.
        """
        button = font.render(text, True, color)
        button_rect = button.get_rect(center=position)
        pygame.draw.rect(screen, color, button_rect.inflate(30, 10), 5, border_radius=25)
        screen.blit(button, (button_rect.x, button_rect.y))
        return button_rect

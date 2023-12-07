from enum import Enum


class GameState(Enum):
    """
    Enumeration representing the various states of the game.
    """
    MAIN_MENU = "main_menu"
    PLAYING = "playing"
    PAUSED = "paused"
    GAME_OVER = "game_over"


class PlayerState(Enum):
    """
    Enumeration representing the various states of the player.
    """
    IDLE = "idle"
    WALKING_RIGHT = "walking_right"
    WALKING_LEFT = "walking_left"
    JUMPING = "jumping"
    SLIDING = "sliding"

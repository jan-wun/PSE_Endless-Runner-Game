from enum import Enum


class GameState(Enum):
    """
    Enumeration representing the various states of the game.
    """
    MAIN_MENU = "main_menu"
    SETTINGS = "settings"
    STATS = "statistics"
    SHOP = "shop"
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


class EnemyType(Enum):
    """
    Enumeration representing the type of an enemy.
    """
    DRONE = "drone"
    ROBOT = "robot"


class EnemyState(Enum):
    IDLE = "idle"
    WALKING_RIGHT = "walking_right"
    WALKING_LEFT = "walking_left"


class WeaponType(Enum):
    DEFAULT = "default"
    UPGRADE = "upgrade"

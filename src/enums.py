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
    CONTROLS = "controls"


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
    Enumeration representing the various types of an enemy.
    """
    DRONE = "drone"
    ROBOT = "robot"


class EnemyState(Enum):
    """
    Enumeration representing the various states of an enemy.
    """
    IDLE = "idle"
    WALKING_RIGHT = "walking_right"
    WALKING_LEFT = "walking_left"


class WeaponType(Enum):
    """
    Enumeration representing the various types of a weapon.
    """
    DEFAULT = "default"
    UPGRADE = "upgrade"


class PowerUpType(Enum):
    """
    Enumeration representing the various types of a power up.
    """
    INVINCIBILITY = "invincibility"
    FREEZE = "freeze"
    MULTIPLE_SHOTS = "multiple_shots"
    SHRINK = "shrink"

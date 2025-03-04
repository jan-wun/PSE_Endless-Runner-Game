import pytest
import pygame
from unittest import mock
from src.enums import PlayerState
from src.assets import Assets


@pytest.fixture(scope="session", autouse=True)
def init_pygame():
    """Initialize pygame before running tests."""
    pygame.init()
    pygame.display.set_mode((800, 600))

@pytest.fixture(scope="session")
def shared_assets():
    """Creates a single shared Assets instance to prevent reloading assets multiple times."""
    assets = Assets()  # Load Assets once per test session
    assets.load_assets()  # Ensure assets are loaded
    return assets  # This will be reused in all tests

@pytest.fixture
def mock_player():
    """Creates a mock player object with necessary attributes."""
    player = mock.Mock()
    player.sprite.position = [100, 520]
    player.rect = pygame.Rect(100, 520, 50, 100)
    player.current_state = PlayerState.IDLE
    player.previous_walking_state = PlayerState.WALKING_RIGHT
    player.weapon = mock.Mock(shots=1)
    player.sprite.weapon.shots = 1
    return player

@pytest.fixture
def mock_game(mock_player, shared_assets):
    """Creates a mock game object with necessary attributes."""
    mock_game = mock.Mock()
    mock_game.width = 800
    mock_game.height = 600
    mock_game.screen = mock.Mock()
    mock_game.screen.get_rect.return_value = pygame.Rect(0, 0, 800, 600)
    mock_game.player = mock_player
    mock_game.projectiles = pygame.sprite.Group()
    mock_game.scrolling_bg_speed = shared_assets.config["scrolling_bg_speed"]
    mock_game.fps = shared_assets.config["fps"]
    mock_game.assets = shared_assets
    return mock_game

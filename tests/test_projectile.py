import pytest
import pygame
from unittest import mock
from src.projectile import Projectile


@pytest.fixture
def sample_projectile(mock_game):
    """Creates a sample projectile for testing."""
    position = [100, 200]
    velocity = [5, 0]  # shot moves to the right
    image_list = [pygame.Surface((10, 10))]  # Dummy image
    shooter = "player"

    return Projectile(position, velocity, image_list, mock_game, shooter)

def test_projectile_initialization(sample_projectile):
    """Tests if the projectile initializes with correct attributes."""
    assert sample_projectile.position == [100, 200]
    assert sample_projectile.velocity == [5, 0]
    assert sample_projectile.shooter == "player"
    assert isinstance(sample_projectile.image_list, list)
    assert len(sample_projectile.image_list) > 0
    assert sample_projectile.image == sample_projectile.image_list[0]

def test_projectile_movement(sample_projectile):
    """Tests if the projectile moves correctly according to its velocity."""
    initial_position = sample_projectile.position.copy()
    sample_projectile.update()

    expected_x = initial_position[0] + sample_projectile.velocity[0]
    expected_y = initial_position[1] + sample_projectile.velocity[1]

    assert sample_projectile.position == [expected_x, expected_y], "Projectile did not move correctly!"

def test_projectile_removal_off_screen(sample_projectile):
    """Tests if the projectile is removed when it moves out of the screen."""
    sample_projectile.position = [-10, -10]  # set projectile position outside the screen
    sample_projectile.rect.topleft = (-10, -10)  # Update rect position to match

    with mock.patch.object(sample_projectile, "kill") as mock_kill:
        sample_projectile.update()
        mock_kill.assert_called_once()  # Check, if `kill()` was called

def test_projectile_gives_shot_back_to_player(sample_projectile, mock_game):
    """Tests if a player gets a shot back when the projectile is removed."""
    sample_projectile.position = [-10, -10]  # set projectile position outside the screen
    sample_projectile.rect.topleft = (-10, -10)  # Update rect position to match
    initial_shots = mock_game.player.sprite.weapon.shots

    sample_projectile.update()

    assert mock_game.player.sprite.weapon.shots == initial_shots + 1, "Player should have received a shot back!"


import pytest
import pygame
from unittest import mock
from src.obstacle import Obstacle


@pytest.fixture
def sample_obstacle(mock_game):
    """Creates a sample obstacle for testing."""
    position = [600, 300]  # Initial position
    images = [pygame.Surface((50, 50))]  # Dummy image
    obstacle_type = 'car'  # example type
    speed = 5  # example speed

    return Obstacle(position, images, obstacle_type, speed, mock_game)

@pytest.mark.parametrize("obstacle_type, speed", [
    ('car', 5),
    ('meteor', 3),
])
def test_obstacle_initialization(mock_game, obstacle_type, speed):
    """Tests if the obstacle initializes with correct attributes."""
    position = [600, 300]
    images = [pygame.Surface((50, 50))]
    obstacle = Obstacle(position, images, obstacle_type, speed, mock_game)

    assert obstacle.type == obstacle_type
    assert obstacle.speed == speed
    assert obstacle.position == position
    assert obstacle.image_list == images
    assert obstacle.image == images[0]

def test_obstacle_moves_correctly(sample_obstacle, mock_game):
    """Tests if the obstacle moves left according to its speed and background speed."""
    initial_x = sample_obstacle.position[0]
    sample_obstacle.move()

    expected_x = initial_x - (mock_game.scrolling_bg_speed + sample_obstacle.speed)
    assert sample_obstacle.position[0] == expected_x, "Obstacle did not move correctly!"

def test_obstacle_kills_itself_when_off_screen(sample_obstacle):
    """Tests if the obstacle is removed when it moves out of the screen."""
    sample_obstacle.position = [-sample_obstacle.image.get_width() - 1, 300]  # Move off-screen left

    with mock.patch.object(sample_obstacle, "kill") as mock_kill:
        sample_obstacle.move()
        mock_kill.assert_called_once()

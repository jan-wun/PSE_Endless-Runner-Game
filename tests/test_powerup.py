import pytest
from src.powerup import PowerUp
from src.enums import PowerUpType
from unittest import mock


@pytest.fixture
def sample_powerup(mock_game):
    """Creates a sample power-up for testing."""
    position = [500, 100]  # Starting position
    powerup_type = PowerUpType.INVINCIBILITY  # Default type for test
    return PowerUp(position, powerup_type, mock_game)

@pytest.mark.parametrize("powerup_type, expected_images", [
    (PowerUpType.INVINCIBILITY, "invincible_powerup"),
    (PowerUpType.FREEZE, "freeze_powerup"),
    (PowerUpType.MULTIPLE_SHOTS, "multiple_shots_power_up"),
    (PowerUpType.SHRINK, "shrink_powerup"),
])
def test_powerup_initialization(mock_game, powerup_type, expected_images):
    """Tests if the power-up initializes correctly with the expected type and image."""
    powerup = PowerUp([500, 100], powerup_type, mock_game)

    assert powerup.type == powerup_type
    assert powerup.fall_speed == powerup.assets.config["power_up_fall_speed"]
    assert powerup.image_list == powerup.assets.__getattribute__(expected_images)
    assert powerup.position == [500, 100]

@pytest.mark.parametrize("powerup_type, expected_effect", [
    (PowerUpType.INVINCIBILITY, lambda game: game.player.sprite.invincible),
    (PowerUpType.FREEZE, lambda game: game.freeze),
    (PowerUpType.MULTIPLE_SHOTS, lambda game: game.player.sprite.weapon.max_shots),
    (PowerUpType.SHRINK, lambda game: game.player.sprite.scale_factor == 0.25),
])
def test_apply_powerup(sample_powerup, mock_game, powerup_type, expected_effect):
    """Tests if the power-up applies the correct effect to the player or game."""
    sample_powerup.type = powerup_type
    sample_powerup.apply_powerup()

    if powerup_type == PowerUpType.MULTIPLE_SHOTS:
        assert mock_game.player.sprite.weapon.max_shots == sample_powerup.assets.config["multiple_shots"]
        assert mock_game.player.sprite.weapon.shots == sample_powerup.assets.config["multiple_shots"]
    elif powerup_type == PowerUpType.SHRINK:
        assert mock_game.player.sprite.scale_factor == 0.25
        assert mock_game.player.sprite.weapon.scale_factor == 0.25
        assert mock_game.player.sprite.rect.height == int(mock_game.player.sprite.original_height * 0.25)
    else:
        assert expected_effect(mock_game) is True

@pytest.mark.parametrize("initial_x, initial_y, move_down", [
    (700, 0, True),  # Power-up starts high and should move left + down
    (700, 500, False),  # Power-up reaches max fall height and should only move left
])
def test_powerup_moves_correctly(sample_powerup, mock_game, initial_x, initial_y, move_down):
    """Tests if the power-up moves left and (conditionally) down correctly."""
    sample_powerup.position = [initial_x, initial_y]  # Set initial test position
    sample_powerup.move()

    # Expected movement
    expected_x = initial_x - mock_game.scrolling_bg_speed
    expected_y = initial_y + sample_powerup.fall_speed if move_down else initial_y

    assert sample_powerup.position == [expected_x, expected_y], (f"PowerUp did not move correctly "
                                                                 f"from X={initial_x} and Y={initial_y}!")

def test_powerup_kills_itself_when_off_screen(sample_powerup):
    """Tests if the power-up is removed when it moves out of the screen."""
    sample_powerup.position = [-sample_powerup.image.get_width() - 1, 100]  # Move off-screen left

    with mock.patch.object(sample_powerup, "kill") as mock_kill:
        sample_powerup.move()
        mock_kill.assert_called_once()

def test_shrink_powerup_expires(mock_game):
    """Tests if the shrink effect expires after the defined time."""
    powerup = PowerUp([500, 100], PowerUpType.SHRINK, mock_game)
    powerup.apply_powerup()

    # Simulate timer countdown
    mock_game.shrink_timer = 1  # Set to 1 frame remaining
    mock_game.update()

    assert mock_game.player.sprite.scale_factor == 1.0  # Player should return to normal size
    assert mock_game.player.sprite.weapon.scale_factor == 1.0

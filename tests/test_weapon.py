import pytest
from src.weapon import Weapon
from src.enums import WeaponType, PlayerState
from tests.conftest import mock_game


@pytest.fixture
def sample_weapon(mock_game):
    """Creates a sample weapon for testing."""
    position = [mock_game.player.sprite.position[0] + mock_game.player.rect.width, mock_game.player.sprite.position[1] + 30]
    weapon_type = WeaponType.DEFAULT
    return Weapon(position, weapon_type, mock_game, mock_game.player)

@pytest.mark.parametrize("weapon_type, expected_projectile, expected_shot_speed, expected_max_shots", [
    (WeaponType.DEFAULT, "default_weapon_bullet", "shot_speed_default_weapon", "shots_default_weapon"),
    (WeaponType.UPGRADE, "upgrade_weapon_bullet", "shot_speed_upgrade_weapon", "shots_upgrade_weapon"),
])
def test_weapon_initialization_with_different_types(mock_game, weapon_type, expected_projectile, expected_shot_speed, expected_max_shots):
    """Tests if the weapon initializes correctly for the two different weapon types."""
    position = [mock_game.player.sprite.position[0] + mock_game.player.rect.width, mock_game.player.sprite.position[1] + 30]
    weapon = Weapon(position, weapon_type, mock_game, mock_game.player)

    assert weapon.type == weapon_type
    assert weapon.projectile_image == weapon.assets.__getattribute__(expected_projectile)
    assert weapon.shot_speed == weapon.assets.config[expected_shot_speed]
    assert weapon.max_shots == weapon.assets.config[expected_max_shots]
    assert weapon.shots == weapon.max_shots
    assert isinstance(weapon.image_list, list)
    assert len(weapon.image_list) > 0
    assert weapon.image == weapon.image_list[0]
    assert weapon.position == [mock_game.player.sprite.position[0] + mock_game.player.rect.width,
                                      mock_game.player.sprite.position[1] + 30]

def test_weapon_fire(sample_weapon, mock_game):
    """Tests if firing the weapon correctly reduces shots and creates a projectile."""
    initial_shots = sample_weapon.shots
    sample_weapon.fire()

    # Ensure shots are reduced by 1
    assert sample_weapon.shots == initial_shots - 1, "Weapon shots count did not decrease!"
    # Ensure a projectile was added to the game
    assert len(mock_game.projectiles) > 0, "Projectile was not added to game.projectiles!"
    # Check if the projectile has the correct image
    last_projectile = list(mock_game.projectiles)[-1]
    assert last_projectile.image == sample_weapon.projectile_image, "Projectile image does not match weapon!"

@pytest.mark.parametrize("player_state, previous_state, expected_x_offset, expected_y_offset", [
    # Walking Left
    (PlayerState.WALKING_LEFT, PlayerState.WALKING_LEFT, -67, 30),  # 67 = rect.width
    (PlayerState.IDLE, PlayerState.WALKING_LEFT, -67, 30),  # IDLE but last was left

    # Walking Right
    (PlayerState.WALKING_RIGHT, PlayerState.WALKING_RIGHT, 50, 30),  # 50 = player.rect.width
    (PlayerState.IDLE, PlayerState.WALKING_RIGHT, 50, 30),  # IDLE but last was right

    # Jumping
    (PlayerState.JUMPING, PlayerState.WALKING_LEFT, -67, 30),
    (PlayerState.JUMPING, PlayerState.WALKING_RIGHT, 50, 30),

    # Sliding
    (PlayerState.SLIDING, PlayerState.WALKING_LEFT, -47, -22),  # -47 = 50 - 67 - 30 (player.rect.width - rect.width - offset)
    (PlayerState.SLIDING, PlayerState.WALKING_RIGHT, 30, -22),  # 22 = rect.height
])
def test_weapon_update_position(sample_weapon, mock_game, player_state, previous_state, expected_x_offset,
                                expected_y_offset):
    """Tests if weapon position updates correctly based on player's state and previous state."""
    # Set player states
    mock_game.player.position = [100, 520]
    mock_game.player.current_state = player_state
    mock_game.player.previous_walking_state = previous_state

    # Update weapon
    sample_weapon.update()

    # Expected position
    expected_x = mock_game.player.sprite.position[0] + expected_x_offset
    expected_y = mock_game.player.sprite.position[1] + expected_y_offset

    # Check if weapon position matches expected values
    assert sample_weapon.position == [expected_x, expected_y], (f"Weapon position incorrect for {player_state} "
                                                                f"with previous {previous_state}!")

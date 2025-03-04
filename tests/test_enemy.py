import pytest
import pygame
from unittest import mock
from src.enemy import Enemy
from src.enums import EnemyType, EnemyState


@pytest.fixture
def enemy_drone(mock_game):
    """Creates a Drone enemy instance for testing."""
    return Enemy([100, 200], EnemyType.DRONE, mock_game)

@pytest.fixture
def enemy_robot(mock_game):
    """Creates a Robot enemy instance for testing."""
    return Enemy([500, 200], EnemyType.ROBOT, mock_game)

def test_enemy_initialization(enemy_drone, enemy_robot):
    """Tests if enemies are correctly initialized with proper attributes."""
    assert enemy_drone.type == EnemyType.DRONE
    assert enemy_robot.type == EnemyType.ROBOT
    assert enemy_drone.speed > 0
    assert enemy_robot.speed > 0
    assert enemy_drone.current_state == EnemyState.IDLE
    assert enemy_robot.current_state == EnemyState.IDLE

def test_enemy_handle_movement_drone(enemy_drone, mock_game):
    """Tests if the drone moves left and right correctly when reaching screen boundaries."""
    # Test 1: Drone starts in the middle and moves to the right
    enemy_drone.position[0] = 400
    enemy_drone.handle_movement()
    assert enemy_drone.position[0] > 400  # Should move right

    # Test 2: Drone reaches right boundary and should start moving to the left
    enemy_drone.position[0] = mock_game.width - enemy_drone.rect.width
    enemy_drone.handle_movement()
    assert enemy_drone.current_state == EnemyState.WALKING_LEFT  # Should switch to moving left

    # Test 3: Drone reaches left boundary and should start moving to the right
    enemy_drone.position[0] = 0
    enemy_drone.handle_movement()
    assert enemy_drone.current_state == EnemyState.WALKING_RIGHT  # Should switch to moving right

def test_enemy_handle_movement_robot(enemy_robot, mock_game):
    """Tests robot movement logic based on player position."""
    mock_game.player.sprite.position = [600, 200]  # Player is to the right
    enemy_robot.handle_movement()
    assert enemy_robot.position[0] > 500  # Should move right

    mock_game.player.sprite.position = [400, 200]  # Player is to the left
    enemy_robot.handle_movement()
    assert enemy_robot.position[0] < 500  # Should move left

def test_enemy_attack(enemy_drone, enemy_robot, mock_game):
    """Tests if an enemy attack creates a projectile and adds it to the game."""
    # Test attack for drone enemy
    enemy_drone.game.projectiles = pygame.sprite.Group()  # Use real sprite group to store projectiles
    enemy_drone.attack_timer = 59  # Ensure attack triggers on the next update
    enemy_drone.assets.config["attack_probability"] = 1  # Set attack probability to 100%
    enemy_drone.attack()
    # Assert that at least one projectile was added for the drone enemy
    assert len(enemy_drone.game.projectiles) > 0, "Expected at least one projectile in projectiles group!"

    # Test attack for robot enemy
    enemy_robot.game.projectiles = pygame.sprite.Group()  # Use real sprite group to store projectiles
    enemy_robot.attack_timer = 59  # Ensure attack triggers on the next update
    enemy_robot.assets.config["attack_probability"] = 1  # Set attack probability to 100%
    enemy_robot.attack()
    # Assert that at least one projectile was added for the robot enemy
    assert len(enemy_robot.game.projectiles) > 0, "Expected at least one projectile in projectiles group!"

def test_enemy_no_attack_if_not_ready(enemy_drone, enemy_robot):
    """Tests that an enemy does NOT attack if the timer condition is not met."""
    # Test no attack for drone enemy
    enemy_drone.game.projectiles = pygame.sprite.Group()  # Real projectile group
    enemy_drone.attack_timer = 10  # Too low for attack to trigger
    enemy_drone.assets.config["attack_probability"] = 1  # Ensure probability is 100%
    enemy_drone.attack()
    assert len(enemy_drone.game.projectiles) == 0, "Enemy should NOT attack if the timer is not ready!"

    # Test no attack for robot enemy
    enemy_robot.game.projectiles = pygame.sprite.Group()  # Real projectile group
    enemy_robot.attack_timer = 10  # Too low for attack to trigger
    enemy_robot.assets.config["attack_probability"] = 1  # Ensure probability is 100%
    enemy_robot.attack()
    assert len(enemy_robot.game.projectiles) == 0, "Enemy should NOT attack if the timer is not ready!"

def test_enemy_update(enemy_robot, enemy_drone):
    """Tests if update()-function calls handle_movement, attack and parent update method correctly."""
    # Update function for drone enemy.
    with mock.patch.object(enemy_drone, "handle_movement") as mock_movement, \
         mock.patch.object(enemy_drone, "attack") as mock_attack, \
            mock.patch("src.entity.Entity.update") as mock_super_update:

        enemy_drone.update()
        mock_movement.assert_called()
        mock_attack.assert_called()
        mock_super_update.assert_called_once()

    # Update function for robot enemy.
    with mock.patch.object(enemy_robot, "handle_movement") as mock_movement, \
         mock.patch.object(enemy_robot, "attack") as mock_attack, \
            mock.patch("src.entity.Entity.update") as mock_super_update:

        enemy_robot.update()
        mock_movement.assert_called()
        mock_attack.assert_called()
        mock_super_update.assert_called_once()

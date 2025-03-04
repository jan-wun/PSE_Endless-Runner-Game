import os
import pytest
import pygame
from unittest import mock
from src.player import Player
from src.enums import PlayerState, WeaponType, GameState


@pytest.fixture
def sample_player(mock_game):
    """Creates a sample player for testing."""
    image_path = "assets/images/"
    images_idle = [pygame.transform.scale_by(
        pygame.image.load(os.path.join(image_path, f"player/idle/idle{i}.png")).convert_alpha(), 4) for i in
        range(1, 5)]
    images_walk = [pygame.transform.scale_by(
        pygame.image.load(os.path.join(image_path, f"player/walk/walk{i}.png")).convert_alpha(), 4) for i in
        range(1, 7)]
    images_jump = [pygame.transform.scale_by(
        pygame.image.load(os.path.join(image_path, f"player/jump/jump{i}.png")).convert_alpha(), 4) for i in
        range(1, 5)]
    images_slide = [pygame.transform.scale_by(
        pygame.image.load(os.path.join(image_path, f"player/slide/slide{i}.png")).convert_alpha(), 4) for i in
        range(1, 2)]
    return Player(images_idle, images_walk, images_jump, images_slide, mock_game)

def test_player_initialization(sample_player, mock_game):
    """Tests if the player initializes correctly with default attributes."""
    assert sample_player.position == [100, 520]
    assert sample_player.health == sample_player.assets.config["initial_player_health"]
    assert isinstance(sample_player.weapon, mock.Mock) or sample_player.weapon.type == WeaponType.DEFAULT
    assert sample_player.current_state == PlayerState.IDLE
    assert not sample_player.is_jumping
    assert not sample_player.is_sliding

def test_player_move_left(sample_player, mock_game):
    """Tests if the player moves left correctly within boundaries."""
    initial_x = sample_player.position[0]
    sample_player.move_left()

    assert sample_player.position[0] < initial_x, "Player should move left!"
    sample_player.position[0] = 0
    sample_player.move_left()
    assert sample_player.position[0] == 0, "Player should not move beyond left boundary!"

def test_player_move_right(sample_player, mock_game):
    """Tests if the player moves right correctly within boundaries."""
    initial_x = sample_player.position[0]
    sample_player.move_right()

    assert sample_player.position[0] > initial_x, "Player should move right!"
    sample_player.position[0] = mock_game.width - sample_player.rect.width
    sample_player.move_right()
    assert sample_player.position[
               0] == mock_game.width - sample_player.rect.width, "Player should not move beyond right boundary!"

def test_player_jump(sample_player):
    """Tests if the player jumps correctly and follows the jump mechanics."""
    sample_player.is_jumping = True
    initial_y = sample_player.position[1]

    sample_player.jump()
    assert sample_player.position[1] < initial_y, "Player should move up when jumping!"

    while sample_player.is_jumping:
        sample_player.jump()

    assert sample_player.position[1] == initial_y, "Player should be at the ground after landing!"
    assert not sample_player.is_jumping, "Player should not be jumping after landing!"

def test_player_slide(sample_player):
    """Tests if the player slides correctly and speed decreases over time."""
    sample_player.previous_walking_state = PlayerState.WALKING_RIGHT
    sample_player.is_sliding = True
    initial_x = sample_player.position[0]

    sample_player.slide()
    assert sample_player.position[0] > initial_x, "Player should move to the side while sliding!"
    assert sample_player.position[1] == sample_player.slide_height, "Player should change height while sliding!"

    while sample_player.is_sliding:
        sample_player.slide()

    assert not sample_player.is_sliding, "Player should stop sliding when speed reaches zero!"
    assert sample_player.position[1] == sample_player.rect.top, "Player should be at same height after sliding!"

def test_player_shoot(sample_player):
    """Tests if the player can shoot only when he has ammo."""
    sample_player.weapon.shots = 1
    with mock.patch.object(sample_player.weapon, "fire") as mock_fire:
        sample_player.shoot()
        mock_fire.assert_called_once()

    sample_player.weapon.shots = 0
    with mock.patch.object(sample_player.weapon, "fire") as mock_fire:
        sample_player.shoot()
        mock_fire.assert_not_called()

def test_player_update(sample_player):
    """Tests if update correctly calls the necessary functions."""
    with mock.patch.object(sample_player, "handle_input") as mock_handle_input, \
            mock.patch.object(sample_player, "jump") as mock_jump, \
            mock.patch.object(sample_player, "slide") as mock_slide, \
            mock.patch.object(sample_player, "update_animation") as mock_update_animation, \
            mock.patch.object(sample_player.weapon, "update") as mock_weapon_update:
        sample_player.update()

        mock_handle_input.assert_called_once()
        mock_jump.assert_called_once()
        mock_slide.assert_called_once()
        mock_update_animation.assert_called_once()
        mock_weapon_update.assert_called_once()

def test_player_reset(sample_player):
    """Tests if the player resets to default state correctly."""
    sample_player.is_jumping = True
    sample_player.is_sliding = True
    sample_player.health = 50
    sample_player.position = [300, 200]
    sample_player.reset()

    assert sample_player.position == [100, 520], "Position should be reset!"
    assert sample_player.health == sample_player.assets.config["initial_player_health"], "Health should be reset!"
    assert not sample_player.is_jumping, "Player should not be jumping after reset!"
    assert not sample_player.is_sliding, "Player should not be sliding after reset!"

def test_handle_input_movement(sample_player):
    """Tests if the player handles movement inputs correctly."""
    sample_player.game.current_state = GameState.PLAYING

    with mock.patch("pygame.key.get_pressed", return_value={
        pygame.K_RIGHT: True, pygame.K_LEFT: False, pygame.K_UP: False, pygame.K_DOWN: False, pygame.K_SPACE: False}):
        sample_player.handle_input()
        assert sample_player.current_state == PlayerState.WALKING_RIGHT, "Player should move right!"

    with mock.patch("pygame.key.get_pressed", return_value={
        pygame.K_LEFT: True, pygame.K_RIGHT: False, pygame.K_UP: False, pygame.K_DOWN: False, pygame.K_SPACE: False}):
        sample_player.handle_input()
        assert sample_player.current_state == PlayerState.WALKING_LEFT, "Player should move left!"

    with mock.patch("pygame.key.get_pressed", return_value={
        pygame.K_LEFT: False, pygame.K_RIGHT: False, pygame.K_UP: False, pygame.K_DOWN: False, pygame.K_SPACE: False}):
        sample_player.handle_input()
        assert sample_player.current_state == PlayerState.IDLE, "Player should be idle when no keys are pressed!"

def test_handle_input_jump(sample_player):
    """Tests if the player correctly starts jumping when pressing UP."""
    sample_player.game.current_state = GameState.PLAYING

    with mock.patch("pygame.key.get_pressed", return_value={
        pygame.K_UP: True, pygame.K_LEFT: False, pygame.K_RIGHT: False, pygame.K_DOWN: False, pygame.K_SPACE: False}):
        sample_player.handle_input()
        assert sample_player.is_jumping, "Player should start jumping when UP key is pressed!"

def test_handle_input_slide(sample_player):
    """Tests if the player correctly starts sliding when pressing DOWN while moving."""
    sample_player.game.current_state = GameState.PLAYING
    sample_player.previous_walking_state = PlayerState.WALKING_RIGHT
    sample_player.slide_cooldown = 0

    with mock.patch("pygame.key.get_pressed", return_value={
        pygame.K_DOWN: True, pygame.K_RIGHT: True, pygame.K_UP: False, pygame.K_LEFT: False, pygame.K_SPACE: False}):
        sample_player.handle_input()
        assert sample_player.is_sliding, "Player should start sliding when DOWN is pressed while moving!"

def test_handle_input_shoot(sample_player):
    """Tests if the player correctly shoots when pressing SPACE."""
    sample_player.game.current_state = GameState.PLAYING
    sample_player.shoot_pressed = False

    with mock.patch("pygame.key.get_pressed", return_value={
        pygame.K_SPACE: True, pygame.K_UP: False, pygame.K_LEFT: False, pygame.K_RIGHT: False, pygame.K_DOWN: False}):
        with mock.patch.object(sample_player, "shoot") as mock_shoot:
            sample_player.handle_input()
            mock_shoot.assert_called_once()
            assert sample_player.shoot_pressed, "Player should not continuously fire when holding SPACE!"

@pytest.mark.parametrize("player_state, should_flip", [
    (PlayerState.IDLE, False),
    (PlayerState.WALKING_LEFT, True),
    (PlayerState.WALKING_RIGHT, False),
    (PlayerState.JUMPING, True),  # If previous walking state was left
    (PlayerState.SLIDING, True)   # If previous walking state was left
])
def test_update_animation(sample_player, player_state, should_flip):
    """Tests if the animation updates correctly based on the player's state."""
    sample_player.current_state = player_state
    # Simulate previous walking state for jumping / sliding
    if player_state in [PlayerState.JUMPING, PlayerState.SLIDING]:
        sample_player.previous_walking_state = PlayerState.WALKING_LEFT if should_flip else PlayerState.WALKING_RIGHT

    sample_player.update_animation()
    expected_images = sample_player.animations[player_state]

    # If necessary, flip images (like function would)
    if should_flip:
        expected_images = [pygame.transform.flip(img, True, False) for img in expected_images]

    # Compare pixel-arrays (actual and expected images)
    for actual_img, expected_img in zip(sample_player.image_list, expected_images):
        actual_pixels = pygame.surfarray.array3d(actual_img)
        expected_pixels = pygame.surfarray.array3d(expected_img)

        assert (actual_pixels == expected_pixels).all(), f"Animation mismatch for state {player_state}!"

def test_update_animation_frame(sample_player):
    """Tests if the animation frame updates correctly."""
    initial_frame = sample_player.current_frame
    sample_player.update_animation_frame()

    assert sample_player.current_frame != initial_frame, "Animation frame should change!"
    assert 0 <= int(sample_player.current_frame) < len(sample_player.image_list), "Frame index should stay within bounds!"

def test_player_invincibility(sample_player):
    """Tests if the player correctly handles invincibility duration."""
    sample_player.invincible = True
    sample_player.invincible_time = 1  # Simulate 1 frame remaining

    sample_player.update()  # 1. Update
    assert sample_player.invincible is True, "Player should still be invincible!"

    sample_player.update()  # 2. Update (Timer should be 0 now)
    assert sample_player.invincible is False, "Player should no longer be invincible!"

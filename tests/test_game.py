import pytest
import pygame
from unittest import mock
from src.game import Game
from src.enums import GameState, WeaponType, EnemyType
from src.player import Player
from src.projectile import Projectile
from src.enemy import Enemy


@pytest.fixture
def mock_game():
    """Creates a mocked game instance for testing."""
    with mock.patch("pygame.display.set_mode"), mock.patch("pygame.init"):
        game = Game(size=[800, 600])
    return game

def test_game_initialization(mock_game):
    """Tests if the game initializes correctly with default values."""
    assert mock_game.width == 800
    assert mock_game.height == 600
    assert mock_game.current_state == GameState.MAIN_MENU
    assert isinstance(mock_game.player.sprite, Player)

def test_game_set_up_run(mock_game):
    """Tests if the game setup initializes correct values."""
    mock_game.set_up_run()
    assert mock_game.distance == 0
    assert mock_game.scrolling_bg_speed == mock_game.assets.config["scrolling_bg_speed"]
    assert not mock_game.freeze

def test_handle_states_and_events_main_menu(mock_game):
    """Tests if the main menu handles input correctly."""
    mock_game.current_state = GameState.MAIN_MENU

    with mock.patch.object(mock_game.main_menu, "display"), \
            mock.patch.object(mock_game.main_menu, "handle_input", return_value="play_button"):
        mock_game.handle_states_and_events(pygame.event.Event(pygame.MOUSEBUTTONUP, {}))

    assert mock_game.current_state == GameState.PLAYING

@pytest.mark.parametrize("button, expected_state", [
    ("resume_button", GameState.PLAYING),
    ("restart_button", GameState.PLAYING),
    ("play_button", GameState.PLAYING),
    ("settings_button", GameState.SETTINGS),
    ("shop_button", GameState.SHOP),
    ("stats_button", GameState.STATS),
    ("controls_button", GameState.CONTROLS),
    ("main_menu_button", GameState.MAIN_MENU),
    ("back_button", GameState.MAIN_MENU),
    ("quit_button", None)  # This should call end_game()
])
def test_handle_button_result(mock_game, button, expected_state):
    """Tests if handle_button_result correctly updates the game state."""
    with mock.patch.object(mock_game, "end_game") as mock_end_game:
        mock_game.handle_button_result(button)

    if expected_state:
        assert mock_game.current_state == expected_state, f"Expected state {expected_state} but got {mock_game.current_state}"
    else:
        mock_end_game.assert_called_once()  # Ensure quit button calls end_game()

@pytest.mark.parametrize("item_name, item_cost, expected_health, expected_weapon, should_fail", [
    ("extra_life", 100, 2, WeaponType.DEFAULT, False),  # Buy extra life successfully
    ("extra_life", 100, 2, WeaponType.DEFAULT, True),   # Try buying again (should fail)
    ("weapon_upgrade", 100, 1, WeaponType.UPGRADE, False), # Buy weapon upgrade successfully
    ("weapon_upgrade", 100, 1, WeaponType.UPGRADE, True),  # Try buying again (should fail)
    ("extra_life", 200, 1, WeaponType.DEFAULT, True),  # Not enough money
    ("weapon_upgrade", 200, 1, WeaponType.DEFAULT, True)  # Not enough money
])
def test_handle_shop_purchase(mock_game, item_name, item_cost, expected_health, expected_weapon, should_fail):
    """Tests if the shop correctly processes purchases and prevents duplicate buys."""
    mock_game.coins = 150 if not should_fail else 50  # Ensure enough or insufficient coins

    with mock.patch("tkinter.messagebox.showinfo") as mock_message:
        mock_game.handle_shop_purchase(item_cost, item_name)

    if should_fail:
        mock_message.assert_called_once()
    else:
        assert mock_game.coins == 150 - item_cost, "Coins should decrease after purchase!"
        assert mock_game.player.sprite.health == expected_health, "Player should receive extra life!"
        assert mock_game.player.sprite.weapon.type == expected_weapon, "Player weapon should be upgraded!"

def test_game_update(mock_game):
    """Tests if the game update function calls necessary updates."""
    with mock.patch.object(mock_game.player, "update") as mock_player_update, \
            mock.patch.object(mock_game.obstacles, "update") as mock_obstacles_update, \
            mock.patch.object(mock_game.enemies, "update") as mock_enemies_update, \
            mock.patch.object(mock_game.projectiles, "update") as mock_projectiles_update:
        mock_game.update()

        mock_player_update.assert_called_once()
        mock_obstacles_update.assert_called_once()
        mock_enemies_update.assert_called_once()
        mock_projectiles_update.assert_called_once()

def test_game_render(mock_game):
    """Tests if the game render function calls necessary blit operations."""
    with mock.patch.object(mock_game.screen, "blit") as mock_blit, \
            mock.patch("pygame.display.flip") as mock_flip:
        mock_game.render()
        assert mock_blit.call_count > 0  # Ensure something was drawn
        mock_flip.assert_called_once()

def test_restart_game(mock_game):
    """Tests if restart_game resets game objects and timers."""
    with mock.patch.object(mock_game, "reset_timers") as mock_reset_timers:
        mock_game.restart_game()
        assert mock_game.current_state == GameState.PLAYING
        assert len(mock_game.obstacles) == 0
        assert len(mock_game.enemies) == 0
        assert len(mock_game.projectiles) == 0
        assert len(mock_game.power_ups) == 0
        mock_reset_timers.assert_called_once()

def test_restart_game_resets_player(mock_game):
    """Tests if restart_game resets player attributes properly."""
    player = mock_game.player.sprite
    player.health = 0  # Simulate damage
    player.weapon.type = WeaponType.UPGRADE  # Simulate weapon change
    mock_game.restart_game()

    assert player.health == 1, "Player health should reset to 1 after restart!"
    assert player.weapon.type == WeaponType.DEFAULT, "Player weapon should reset to default!"

@pytest.mark.parametrize("sprite_type, should_collide", [
    ("player", True),  # Player collides with an obstacle
    ("enemy", True),  # Enemy collides with a projectile
    ("player_projectile", True),  # Player gets hit by an enemy projectile
    ("player", False),  # Player does NOT collide with anything
    ("enemy", False),  # Enemy does NOT collide with a projectile
    ("player_projectile", False)  # Enemy projectile misses the player
])
def test_check_collision(mock_game, sprite_type, should_collide):
    """Tests if check_collision correctly detects and handles collisions for different object types."""

    if sprite_type == "player":
        # Use the real player instance from the game
        test_sprite = mock_game.player.sprite
        test_sprite.rect = pygame.Rect(100, 100, 50, 50)  # Set player's position and size

        # Create an obstacle that either collides with the player or does not
        obstacle = pygame.sprite.Sprite()
        obstacle.rect = pygame.Rect(100, 100, 50, 50) if should_collide else pygame.Rect(300, 300, 50, 50)
        sprite_group = pygame.sprite.Group(obstacle)  # Add obstacle to a sprite group

    elif sprite_type == "enemy":
        # Create an enemy instance
        test_sprite = Enemy(position=[100, 100], enemy_type=EnemyType.ROBOT, game=mock_game)
        test_sprite.rect = pygame.Rect(100, 100, 50, 50)  # Set enemy position and size

        # Create a projectile that either hits the enemy or misses
        velocity = [5, 0]  # Example velocity
        image_list = [pygame.Surface((10, 10))]  # Placeholder image
        projectile = Projectile(position=[100, 100] if should_collide else [300, 300],
                                velocity=velocity,
                                shooter="player",
                                image_list=image_list,
                                game=mock_game)
        projectile.rect = pygame.Rect(100, 100, 50, 50) if should_collide else pygame.Rect(300, 300, 50, 50)
        sprite_group = pygame.sprite.Group(projectile)  # Add projectile to a sprite group

    elif sprite_type == "player_projectile":
        test_sprite = mock_game.player.sprite  # The player
        test_sprite.rect = pygame.Rect(100, 100, 50, 50)  # Set player's position

        # Enemy projectile
        velocity = [-5, 0]  # Moving towards the player
        image_list = [pygame.Surface((10, 10))]  # Placeholder image
        enemy_projectile = Projectile(position=[100, 100] if should_collide else [300, 300],
                                      velocity=velocity,
                                      shooter="enemy",
                                      image_list=image_list,
                                      game=mock_game)
        enemy_projectile.rect = pygame.Rect(100, 100, 50, 50) if should_collide else pygame.Rect(300, 300, 50, 50)
        sprite_group = pygame.sprite.Group(enemy_projectile)  # Add projectile to a sprite group

    if sprite_type == "enemy":
        # Mock the `kill()` method to verify that an enemy and projectile are both removed on collision
        with mock.patch.object(test_sprite, "kill") as mock_enemy_kill, \
                mock.patch.object(projectile, "kill") as mock_projectile_kill:
            mock_game.check_collision(test_sprite, sprite_group)

        if should_collide:
            # If a collision is expected, both the enemy and projectile should be removed
            mock_enemy_kill.assert_called_once()
            mock_projectile_kill.assert_called_once()
        else:
            # If no collision is expected, neither object should be removed
            mock_enemy_kill.assert_not_called()
            mock_projectile_kill.assert_not_called()

    elif sprite_type == "player_projectile":
        # Mock `handle_player_collision` to verify that it is triggered on enemy projectile hit
        with mock.patch.object(mock_game, "handle_player_collision") as mock_handle_collision:
            mock_game.check_collision(test_sprite, sprite_group)

        if should_collide:
            mock_handle_collision.assert_called_once()
        else:
            mock_handle_collision.assert_not_called()

    else:  # Case: Player colliding with an obstacle
        # Mock `handle_player_collision` to verify that it's called when needed
        with mock.patch.object(mock_game, "handle_player_collision") as mock_handle_collision:
            mock_game.check_collision(test_sprite, sprite_group)

        if should_collide:
            # If collision occurs, `handle_player_collision` should be triggered
            mock_handle_collision.assert_called_once()
        else:
            # If no collision occurs, `handle_player_collision` should NOT be called
            mock_handle_collision.assert_not_called()

def test_handle_player_collision(mock_game):
    """Tests if player collision correctly reduces health and triggers game over."""
    player = mock_game.player.sprite
    player.health = 2  # Start with 2 lifes

    mock_game.handle_player_collision()
    assert player.health == 1, "Player should lose one life upon collision!"

    mock_game.handle_player_collision()
    assert mock_game.current_state == GameState.GAME_OVER, "Game should be over when player reaches 0 health!"

def test_end_game(mock_game):
    """Tests if the game ends properly by calling quit and sys.exit."""
    with mock.patch("pygame.quit") as mock_quit, \
            mock.patch("sys.exit") as mock_exit:
        mock_game.end_game()
        mock_quit.assert_called_once()
        mock_exit.assert_called_once()

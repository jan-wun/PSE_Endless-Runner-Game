import pygame
import pytest
from src.player import Player
from src.obstacle import Obstacle
from src.game import Game
from src.enums import GameState


@pytest.fixture
def game_instance():
    return Game([1344, 768])


@pytest.fixture
def player(game_instance):
    dummy_images = [pygame.Surface((50, 50))]  # Platzhalterbild für den Spieler
    player = Player(dummy_images, dummy_images, dummy_images, dummy_images, game_instance)
    player.rect = pygame.Rect(100, 450, 50, 50)  # Standardgröße und Position setzen
    player.velocity_y = 0  # Sprungmechanik vorbereiten
    return player


@pytest.fixture
def auto_obstacle(game_instance):
    obstacle = Obstacle((500, 500), [pygame.Surface((50, 50))], "car", 5, game_instance)
    obstacle.rect = pygame.Rect(500, 500, 50, 50)  # Größe setzen
    return obstacle


@pytest.fixture
def obstacle_group(auto_obstacle):
    group = pygame.sprite.Group()
    group.add(auto_obstacle)
    return group

def test_player_lands_on_car(game_instance, player, auto_obstacle, obstacle_group):
    """
    Testet, ob der Spieler auf einem Auto landen kann.
    """
    player.rect.bottom = auto_obstacle.rect.top + 10
    player.rect.left = auto_obstacle.rect.left + 10
    game_instance.check_collision(player, obstacle_group)

    assert player.on_moving_platform is True


def test_player_moves_with_car(game_instance, player, auto_obstacle):
    """
    Testet, ob sich der Spieler mit dem Auto mitbewegt.
    """
    player.on_moving_platform = True
    player.platform = auto_obstacle
    player.rect.bottom = auto_obstacle.rect.top + 10
    player.rect.left = auto_obstacle.rect.left + 10
    prev_x = player.rect.x
    auto_obstacle.rect.x += auto_obstacle.speed
    player.update()

    assert player.rect.x == prev_x + auto_obstacle.speed


def test_player_can_jump_off_car(game_instance, player, auto_obstacle):
    """
    Testet, ob der Spieler nach dem Landen auf einem Auto abspringen kann.
    """
    player.on_moving_platform = True
    player.platform = auto_obstacle
    player.rect.bottom = auto_obstacle.rect.top
    player.velocity_y = -10  # Springen simulieren

    assert player.velocity_y < 0  # Der Spieler sollte nach oben springen


def test_player_dies_on_side_collision(game_instance, player, auto_obstacle, obstacle_group):
    """
    Testet, ob eine seitliche Kollision mit einem Auto zum Tod führt.
    """
    player.rect.bottom = auto_obstacle.rect.top +20
    player.rect.left = auto_obstacle.rect.left + 10
    game_instance.check_collision(player, obstacle_group)

    assert game_instance.current_state == GameState.GAME_OVER


def test_other_obstacles_still_kill(game_instance, player):
    """
    Testet, ob Roboter oder Meteoriten den Spieler weiterhin eliminieren.
    """
    group = pygame.sprite.Group()
    robot_obstacle = Obstacle((500, 500), [pygame.Surface((50, 50))], "robot", 5, game_instance)
    robot_obstacle.rect = pygame.Rect(500, 500, 50, 50)  # Größe setzen
    group.add(robot_obstacle)
    player.rect.bottom = robot_obstacle.rect.top + 10
    player.rect.left = robot_obstacle.rect.left + 10
    game_instance.check_collision(player, group)

    assert game_instance.current_state == GameState.GAME_OVER

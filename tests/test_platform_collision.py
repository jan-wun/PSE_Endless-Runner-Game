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
    return Player([], [], [], [], game_instance)


@pytest.fixture
def auto_obstacle(game_instance):
    return Obstacle((500, 500), [], "car", 5, game_instance)


def test_player_lands_on_car(game_instance, player, auto_obstacle):
    """
    Testet, ob der Spieler auf einem Auto landen kann.
    """
    player.rect.bottom = auto_obstacle.rect.top
    player.velocity_y = 5  # Fallgeschwindigkeit simulieren
    game_instance.check_collision(player, [auto_obstacle])

    assert player.on_moving_platform is True


def test_player_moves_with_car(game_instance, player, auto_obstacle):
    """
    Testet, ob sich der Spieler mit dem Auto mitbewegt.
    """
    player.on_moving_platform = True
    player.rect.bottom = auto_obstacle.rect.top
    prev_x = player.rect.x
    auto_obstacle.rect.x += auto_obstacle.speed
    game_instance.update()

    assert player.rect.x == prev_x + auto_obstacle.speed


def test_player_can_jump_off_car(game_instance, player, auto_obstacle):
    """
    Testet, ob der Spieler nach dem Landen auf einem Auto abspringen kann.
    """
    player.on_moving_platform = True
    player.rect.bottom = auto_obstacle.rect.top
    player.jump()

    assert player.velocity_y < 0  # Der Spieler sollte nach oben springen


def test_player_dies_on_side_collision(game_instance, player, auto_obstacle):
    """
    Testet, ob eine seitliche Kollision mit einem Auto zum Tod führt.
    """
    player.rect.right = auto_obstacle.rect.left
    game_instance.check_collision(player, [auto_obstacle])

    assert game_instance.current_state == GameState.GAME_OVER


def test_other_obstacles_still_kill(game_instance, player):
    """
    Testet, ob Roboter oder Meteoriten den Spieler weiterhin eliminieren.
    """
    robot_obstacle = Obstacle((500, 500), [], "robot", 5, game_instance)
    player.rect.bottom = robot_obstacle.rect.top
    game_instance.check_collision(player, [robot_obstacle])

    assert game_instance.current_state == GameState.GAME_OVER

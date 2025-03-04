import pytest
import pygame
from unittest import mock
from src.menu import Menu, MainMenu, SettingsMenu, StatsMenu, GameOverMenu, PauseMenu


@pytest.fixture
def sample_menu(mock_game):
    """Creates a generic menu instance for testing."""
    mock_game.number_of_runs = 5
    mock_game.save_load_manager.load_game_data.return_value = [100, [1, 10, 2, 20, 3, 30]]  # Highscore & run data
    return Menu(mock_game)

def test_menu_initialization(sample_menu):
    """Tests if the menu initializes correctly with empty buttons and sliders."""
    assert sample_menu.buttons == []
    assert sample_menu.sliders == []
    assert sample_menu.center == (672, 384)
    assert isinstance(sample_menu.game, mock.Mock)

def test_menu_handle_input_buttons(sample_menu):
    """Tests if button interactions are correctly detected and processed."""
    mock_button = mock.Mock()
    mock_button.name = "play_button"
    sample_menu.buttons = [mock_button]

    event = pygame.event.Event(pygame.MOUSEBUTTONUP, {"pos": (400, 300)})
    result = sample_menu.handle_input(event)

    assert result == "play_button"

def test_menu_handle_input_sliders(sample_menu):
    """Tests if sliders correctly react to mouse interactions."""
    mock_slider = mock.Mock()
    mock_slider.container_rect.collidepoint.return_value = True
    sample_menu.sliders = [mock_slider]

    # Simulate mouse press event
    with mock.patch("pygame.mouse.get_pressed", return_value=(True, False, False)):
        event_down = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {"pos": (400, 300)})
        sample_menu.handle_input(event_down)

        assert mock_slider.grabbed is True, "Slider should be grabbed after MOUSEBUTTONDOWN!"

    # Simulate mouse release event
    with mock.patch("pygame.mouse.get_pressed", return_value=(False, False, False)):
        event_up = pygame.event.Event(pygame.MOUSEBUTTONUP, {"pos": (400, 300)})
        sample_menu.handle_input(event_up)

        assert mock_slider.grabbed is False, "Slider should not be grabbed after MOUSEBUTTONUP!"

@pytest.fixture
def main_menu(mock_game):
    """Creates a MainMenu instance for testing."""
    return MainMenu(mock_game)

def test_main_menu_buttons(main_menu):
    """Tests if MainMenu initializes with the correct button set."""
    button_names = [button.name for button in main_menu.buttons]
    assert "play_button" in button_names
    assert "quit_button" in button_names
    assert "settings_button" in button_names
    assert "shop_button" in button_names

@pytest.fixture
def settings_menu(mock_game):
    """Creates a SettingsMenu instance for testing."""
    return SettingsMenu(mock_game)

def test_settings_menu_sliders(settings_menu):
    """Tests if SettingsMenu contains the required volume sliders."""
    assert len(settings_menu.sliders) == 2
    slider_names = [slider.name for slider in settings_menu.sliders]
    assert "music_slider" in slider_names
    assert "volume_slider" in slider_names

def test_settings_menu_slider_interaction(settings_menu):
    """Tests if adjusting the music slider correctly modifies the volume."""
    mock_slider = settings_menu.sliders[0]
    with mock.patch.object(Menu, "handle_input", return_value=None):
        with mock.patch.object(mock_slider, "get_value", return_value=50):
            settings_menu.handle_input(pygame.event.Event(pygame.MOUSEBUTTONDOWN, {"pos": (400, 300)}))

    assert settings_menu.assets.music.get_volume() == 0.5, "Music volume should be set to 0.5"

@pytest.fixture
def stats_menu(mock_game):
    """Creates a StatsMenu instance for testing."""
    # Ensure load_game_data returns a proper tuple (highscore, run_distance_list)
    mock_game.save_load_manager.load_game_data.return_value = (100, [1, 10, 2, 20, 3, 30])  # Simulated runs
    return StatsMenu(mock_game)

def test_stats_menu_highscore(stats_menu):
    """Tests if StatsMenu correctly retrieves and displays the highscore."""
    highscore, run_distance_df, _ = stats_menu.get_highscore_and_run_distance()
    assert highscore == 100
    assert not run_distance_df.empty
    assert list(run_distance_df.columns) == ["Run", "Distance"]

@pytest.fixture
def game_over_menu(mock_game):
    """Creates a GameOverMenu instance for testing."""
    return GameOverMenu(mock_game)

def test_game_over_menu_buttons(game_over_menu):
    """Tests if GameOverMenu initializes with the correct buttons."""
    button_names = [button.name for button in game_over_menu.buttons]
    assert "restart_button" in button_names
    assert "quit_button" in button_names
    assert "main_menu_button" in button_names

@pytest.fixture
def pause_menu(mock_game):
    """Creates a PauseMenu instance for testing."""
    return PauseMenu(mock_game)

def test_pause_menu_buttons(pause_menu):
    """Tests if PauseMenu contains the correct buttons for pausing/resuming the game."""
    button_names = [button.name for button in pause_menu.buttons]
    assert "resume_button" in button_names
    assert "main_menu_button" in button_names
    assert "quit_button" in button_names

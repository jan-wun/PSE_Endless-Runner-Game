import os
import pytest
import pygame
from unittest import mock
from src.assets import Assets


@pytest.fixture
def assets_instance():
    """Creates an instance of Assets for testing."""
    with mock.patch.object(Assets, "load_assets"):  # Prevents automatic asset loading
        return Assets()

def test_assets_singleton(assets_instance):
    """Tests if Assets follows the Singleton pattern."""
    another_instance = Assets()
    assert assets_instance is another_instance  # Should be the same instance

def test_load_config(assets_instance):
    """Tests if config.json loads correctly."""
    assets_instance.load_config()
    assert isinstance(assets_instance.config, dict)  # Should be a dictionary
    assert "image_path" in assets_instance.config
    assert "audio_path" in assets_instance.config
    assert "font_path" in assets_instance.config

def test_load_image(assets_instance):
    """Tests if an actual image loads correctly from disk."""
    assets_instance.load_config()  # Ensures image_path is known
    assets_instance.background_image = pygame.image.load(os.path.join(
        assets_instance.config["image_path"], "background.png"))  # Load background image from image_path as example

    assert assets_instance.background_image is not None
    assert isinstance(assets_instance.background_image, pygame.Surface)

def test_load_sound(assets_instance):
    """Tests if a sound loads correctly using pygame.mixer.Sound()."""
    assets_instance.load_config()  # Ensures audio_path is known
    assets_instance.music = pygame.mixer.Sound(os.path.join(assets_instance.config["audio_path"], "music.mp3")) # Load music from audio_path as example

    assert assets_instance.music is not None
    assert isinstance(assets_instance.music, pygame.mixer.Sound)

def test_load_font(assets_instance):
    """Tests if a font loads correctly using pygame.font.Font()."""
    assets_instance.load_config()  # Ensures font_path is known
    assets_instance.font = pygame.font.Font(os.path.join(assets_instance.config["font_path"], "stacker.ttf"), 100) # Load font from font_path as example

    assert assets_instance.font is not None
    assert isinstance(assets_instance.font, pygame.font.Font)

def test_scaled_image(assets_instance, monkeypatch):
    """Tests if an image scales correctly."""
    initial_image_size = assets_instance.background_image.get_size()
    scaled_image = pygame.transform.scale_by(assets_instance.background_image, 2)  # Scale background image as example
    assert scaled_image.get_size() == tuple(x * 2 for x in initial_image_size) # Scaled image should be twice as big

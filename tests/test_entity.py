import pytest
import pygame
from src.entity import Entity
from src.enums import EnemyState


@pytest.fixture
def entity_instance(mock_game):
    """Creates a sample entity for testing."""
    test_position = [100, 200]
    test_images = [pygame.Surface((50, 50)), pygame.Surface((50, 50))]  # Dummy images
    test_state = EnemyState.IDLE  # Placeholder state

    return Entity(test_position, test_images, test_state, mock_game)

def test_entity_initialization(entity_instance):
    """Tests if the entity initializes with the correct attributes."""
    assert entity_instance.position == [100, 200]
    assert isinstance(entity_instance.image_list, list)
    assert len(entity_instance.image_list) > 0
    assert entity_instance.image == entity_instance.image_list[0]
    assert entity_instance.rect.topleft == (100, 200)  # Ensures rect is positioned correctly
    assert entity_instance.current_state == EnemyState.IDLE

def test_entity_update(entity_instance):
    """Tests if update() correctly updates the rect position."""
    entity_instance.position = [300, 400]  # Change position
    entity_instance.update()

    assert entity_instance.rect.topleft == (300, 400)  # rect should match new position

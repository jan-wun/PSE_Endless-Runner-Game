import pytest
import os
from src.manager import SaveLoadSystem


@pytest.fixture
def save_load_system(tmp_path):
    """Creates a SaveLoadSystem instance using a temporary directory."""
    return SaveLoadSystem(file_extension=".save", save_folder=str(tmp_path))

def test_initialization(save_load_system):
    """Tests if the SaveLoadSystem initializes correctly."""
    assert save_load_system.file_extension == ".save"
    assert os.path.exists(save_load_system.save_folder), "Save folder should exist."

def test_save_and_load_data(save_load_system):
    """Tests if data is correctly saved and loaded."""
    data = {"score": 100, "coins": 50}
    filename = "test_file"
    save_load_system.save_data(data, filename)
    loaded_data = save_load_system.load_data(filename)

    assert loaded_data == data, "Loaded data does not match saved data!"

def test_check_for_file(save_load_system):
    """Tests if check_for_file correctly detects existing and missing files."""
    filename = "test_file"
    save_load_system.save_data({"test": "data"}, filename)

    assert save_load_system.check_for_file(filename), "File should exist after saving!"
    assert not save_load_system.check_for_file("non_existent"), "File should not exist!"

def test_load_game_data_with_default(save_load_system):
    """Tests if missing files return the default values."""
    default_values = [0, "No Data"]
    loaded_data = save_load_system.load_game_data(["missing_file1", "missing_file2"], default_values)

    assert loaded_data == default_values, "Should return default values when files are missing!"

def test_load_game_data_with_existing_file(save_load_system):
    """Tests if existing files are loaded correctly and missing ones return default values."""
    save_load_system.save_data(100, "score")
    save_load_system.save_data("Player1", "player_name")
    loaded_data = save_load_system.load_game_data(["score", "missing_file"], [0, "No Name"])

    assert loaded_data == [100, "No Name"], "Should load existing file and return default for missing one!"

def test_save_game_data_overwrite(save_load_system):
    """Tests if game data is saved correctly in 'wb' mode (overwrite)."""
    save_load_system.save_game_data([100, "Player1"], ["score", "player_name"], ["wb", "wb"])

    assert save_load_system.load_data("score") == 100
    assert save_load_system.load_data("player_name") == "Player1"

def test_save_game_data_append(save_load_system):
    """Tests if game data is appended correctly in 'ab' mode."""
    save_load_system.save_data([50], "score")
    save_load_system.save_game_data([[30]], ["score"], ["ab"])

    assert save_load_system.load_data("score") == [50, 30], "Appending data should work correctly!"

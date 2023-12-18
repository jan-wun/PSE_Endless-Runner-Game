import pickle
import os


class SaveLoadSystem:
    def __init__(self, file_extension, save_folder):
        """
        Initializes a SaveLoadSystem instance.

        Args:
            file_extension (str): The file extension to be used for saved files.
            save_folder (str): The folder where saved files will be stored.
        """
        self.file_extension = file_extension
        self.save_folder = save_folder

    def save_data(self, data, name):
        """
        Saves data to a file.

        Args:
            data: The data to be saved.
            name (str): The name of the file (excluding the extension).
        """
        data_file = open(f"{self.save_folder}/{name}{self.file_extension}", "wb")
        pickle.dump(data, data_file)

    def load_data(self, name):
        """
        Loads data from a file.

        Args:
            name (str): The name of the file (excluding the extension).

        Returns:
            The loaded data.
        """
        data_file = open(f"{self.save_folder}/{name}{self.file_extension}", "rb")
        data = pickle.load(data_file)
        return data

    def check_for_file(self, name):
        """
        Checks if a file with the given name exists in the save folder.

        Parameters:
            name (str): The name of the file (excluding the extension).

        Returns:
            True if the file exists, False otherwise.
        """
        return os.path.exists(f"{self.save_folder}/{name}{self.file_extension}")

    def load_game_data(self, files_to_load, default_data):
        """
        Loads game data from files, providing default values if a file is missing.

        Parameters:
            files_to_load (list): A list of file names to load data from.
            default_data (list): A list of default values corresponding to each file.

        Returns:
            A tuple of loaded data or a single variable.
        """
        variables = []
        for index, file in enumerate(files_to_load):
            if self.check_for_file(file):
                variables.append(self.load_data(file))
            else:
                variables.append(default_data[index])

        if len(variables) > 1:
            return tuple(variables)
        else:
            return variables[0]

    def save_game_data(self, data_to_save, file_names):
        """
        Saves game data to files.

        Parameters:
            data_to_save (list): A list of data to be saved.
            file_names (list): A list of file names to save data into.
        """
        for index, file in enumerate(data_to_save):
            self.save_data(file, file_names[index])

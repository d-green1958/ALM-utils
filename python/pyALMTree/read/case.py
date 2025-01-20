from . import turbineOutput
import os
import warnings


class CaseReader:
    """
    A utility class for reading and processing case directories.

    This class provides methods to handle turbine output files and post-processing data
    for a simulation case. It verifies the existence of key directories and allows
    streamlined access to file-specific operations.

    Attributes:
        path (str): The root directory of the case.
        name (str): The name of the case directory (basename of the path).
        turbineOutput_path (str): Path to the "turbineOutput/0" directory.
        postProcessing_path (str): Path to the "postProcessing" directory.
    """

    def __init__(self, path_):
        """
        Initializes the CaseReader with the specified case directory.

        Args:
            path_ (str): Path to the root directory of the case.

        Raises:
            UserWarning: If the "turbineOutput/0" or "postProcessing" directories do not exist.
        """
        self.path = path_
        self.name = os.path.basename(path_)

        self.turbineOutput_path = os.path.join(path_, "turbineOutput", "0")
        if not os.path.exists(self.turbineOutput_path):
            warnings.warn(f"The file turbineOutput does not exist!", UserWarning)

        self.postProcessing_path = os.path.join(path_, "postProcessing")
        if not os.path.exists(self.postProcessing_path):
            warnings.warn(f"The file postProcessing does not exist!", UserWarning)

    def set_path(self, path_):
        """
        Updates the path for the case directory.

        Args:
            path_ (str): The new path to the root directory of the case.
        """
        self.path = path_

    def turbineOutput(self, file_name, blade_data_file=False):
        """
        Processes a turbine output file and returns its data as a DataFrame.

        Args:
            file_name (str): Name of the turbine output file.
            blade_data_file (bool, optional): If True, specifies that the file contains
                                              blade-specific data. Defaults to False.

        Raises:
            FileNotFoundError: If the specified file does not exist in the turbineOutput directory.

        Returns:
            pd.DataFrame: DataFrame containing the turbine output data.
        """
        file_path = os.path.join(self.turbineOutput_path, file_name)
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"{file_name} cannot be found!")
        return turbineOutput.turbineOutput_file(
            file_path, blade_data_file=blade_data_file
        )
    
    def turbineOutput_exists(self):
        """
        check if turbineOutput exists

        Args:
            
        Returns:
            bool: bool representing if turbineOutput exists 
        """
        return os.path.exists(self.turbineOutput_path)
    
    def postProcessing_exists(self):
        """
        check if postProcessing exists

        Args:
            
        Returns:
            bool: bool representing if turbineOutput exists 
        """
        return os.path.exists(self.postProcessing_path)

    def __str__(self):
        """
        Returns a string representation of the CaseReader instance.

        Returns:
            str: A string indicating the name of the case directory.
        """
        return f"CaseReader: {self.name}"


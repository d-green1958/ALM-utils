from . import turbineOutput
from . import postProcessing_sample
from . import postProcessing_probe
import os
import warnings
import pandas as pd
import numpy as np
from typing import Dict


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

    def __init__(self, path_, warnings_on=True):
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
            if warnings_on:
                warnings.warn(f"The file turbineOutput does not exist!", UserWarning)
            self.turbineOutput_files = None
        else:
            self.turbineOutput_files = os.listdir(self.turbineOutput_path)

        self.postProcessing_path = os.path.join(path_, "postProcessing")
        if not os.path.exists(self.postProcessing_path):
            if warnings_on:
                warnings.warn(f"The file postProcessing does not exist!", UserWarning)
            self.postProcessing_files = None
        else:
            self.postProcessing_files = os.listdir(self.postProcessing_path)

    def set_path(self, path_):
        """
        Updates the path for the case directory.

        Args:
            path_ (str): The new path to the root directory of the case.
        """
        self.path = path_

    def turbineOutput(self, file_name, blade_data_file=False, change_time_dir_to=""):
        """
        Processes a turbine output file and returns its data as a DataFrame.

        Args:
            file_name (str): Name of the turbine output file.
            blade_data_file (bool, optional): If True, specifies that the file contains
                                              blade-specific data. Defaults to False.
            change_time_dir_to (str, optional): If provided, the time directory will be 
                                                changed from 0 to the provided value.

        Raises:
            FileNotFoundError: If the specified file does not exist in the turbineOutput directory.

        Returns:
            pd.DataFrame: DataFrame containing the turbine output data.
        """
        file_path = os.path.join(self.turbineOutput_path, file_name)

        if change_time_dir_to != "":
            file_path = os.path.join(
                self.turbineOutput_path, "..", change_time_dir_to, file_name
            )

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

    def postProcessing_sample(
        self,
        sample_subdir_name: str,
        read_variables: list[str],
        target_time: float,
        avoid_variables: list[str] = [],
    ) -> Dict[str, pd.DataFrame]:
        sample_subdir_path = os.path.join(self.postProcessing_path, sample_subdir_name)
        if not os.path.exists(sample_subdir_path):
            raise FileExistsError(f"Cannot find dir: {sample_subdir_path}")

        times_str = os.listdir(sample_subdir_path)
        times_float = np.array(times_str, dtype=float)
        time_ind = np.argmin(np.abs(times_float - target_time))

        time_dir_name = times_str[time_ind]
        time_dir_path = os.path.join(sample_subdir_path, time_dir_name)

        file_names = os.listdir(time_dir_path)
        data_dict = {}
        for file_name in file_names:
            if not any(var in file_name for var in read_variables):
                continue

            if any(var in file_name for var in avoid_variables):
                continue

            file_path = os.path.join(time_dir_path, file_name)
            data_dict[file_name] = postProcessing_sample.postProcessing_sample_file(
                file_path
            )

        return data_dict

    def postProcessing_probe(
        self,
        probe_subdir_name: str,
        read_variables: list[str],
        probe_start_time: str = "0",
        avoid_variables: list[str] = [],
    ) -> Dict[str, Dict[str, any]]:
        probe_subdir_path = os.path.join(
            self.postProcessing_path, probe_subdir_name, probe_start_time
        )
        if not os.path.exists(probe_subdir_path):
            raise FileExistsError(f"Cannot find dir: {probe_subdir_path}")

        file_names = os.listdir(probe_subdir_path)
        data_dict = {}
        for file_name in file_names:
            if not any(var in file_name for var in read_variables):
                continue

            if any(var in file_name for var in avoid_variables):
                continue

            file_path = os.path.join(probe_subdir_path, file_name)
            df = postProcessing_probe.postProcessing_probe_file(file_path)
            data_dict[file_name] = df

        return data_dict

    def __str__(self):
        """
        Returns a string representation of the CaseReader instance.

        Returns:
            str: A string indicating the name of the case directory.
        """
        return f"CaseReader: {self.name}"

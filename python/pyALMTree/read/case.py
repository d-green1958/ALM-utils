from . import turbineOutput
import os
import warnings


class CaseReader:
    def __init__(self, path_):
        self.path = path_
        self.name = os.path.basename(path_)

        self.turbineOutput_path = os.path.join(path_, "turbineOutput", "0")
        if not os.path.exists(self.turbineOutput_path):
            warnings.warn(f"The file turbineOutput does not exist!", UserWarning)

        self.postProcessing_path = os.path.join(path_, "postProcessing")
        if not os.path.exists(self.postProcessing_path):
            warnings.warn(f"The file postProcessing does not exist!", UserWarning)

    def set_path(self, path_):
        self.path = path_

    def turbineOutput(self, file_name, blade_data_file=False):
        file_path = os.path.join(self.turbineOutput_path, file_name)
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"{file_name} cannot be found!")
        return turbineOutput.turbineOutput_file(
            file_path, blade_data_file=blade_data_file
        )

    def __str__(self):
        return f"CaseReader: {self.name}"

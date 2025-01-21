import pandas as pd
import numpy as np
import os
import re


def postProcessing_probe_file(file_path: str) -> pd.DataFrame:
    variable_name = os.path.basename(file_path)

    with open(file_path, "r") as file:
        lines = file.readlines()

    # first read in the locations of the probes and the delimiter to use
    probe_indices = []
    x_coords = []
    y_coords = []
    z_coords = []

    # Regex to extract probe information
    probe_pattern = re.compile(
        r"# Probe (\d+) \((-?\d+\.\d+|\d+) (-?\d+\.\d+|\d+) (-?\d+\.\d+|\d+)\)"
    )

    # Parse each line
    with open(file_path, "r") as file:
        for line in file:
            if not line.startswith("#"):
                if "(" not in line:
                    delimiter = "   "
                    file_type = "scalar"
                else:
                    delimiter = "                "
                    file_type = "vector/tensor"
                break  # Stop processing further lines
            if "Time" in line:
                continue
            if "# Not Found" in line:
                continue
            if "(" not in line:
                # find the delimiter
                continue

            match = probe_pattern.match(line)
            if match:
                probe_indices.append(int(match.group(1)))
                x_coords.append(float(match.group(2)))
                y_coords.append(float(match.group(3)))
                z_coords.append(float(match.group(4)))

    df = pd.read_csv(file_path, comment="#", delimiter=delimiter, engine='python')
    number_of_columns = len(df.columns) - 1
    headers = ["time"]
    for i in range(number_of_columns):
        headers.append(f"Probe {i}")

    df.columns = headers

    x_coords = np.array(x_coords)
    y_coords = np.array(y_coords)
    z_coords = np.array(z_coords)

    for column in df.keys():
        if column == "time":
            continue
        if file_type == "vector/tensor":
            df[column] = df[column].apply(lambda x: x.strip("(").strip(")").split(" "))

    processed_dict = {"time": df["time"].to_numpy()}
    for column in df.keys():
        if column == "time":
            continue
        probe_ind = int(column.strip("Probe").strip(" "))
        probe_dict = {
            "x": x_coords[probe_ind],
            "y": y_coords[probe_ind],
            "z": z_coords[probe_ind],
        }
        print("here", file_type)
        if file_type == "vector/tensor":
            n = len(df[column][0])
            arrays_by_index = [np.array(df[column].apply(lambda x: x[i])) for i in range(n)]
            for i in range(n):
                probe_dict[f"{variable_name}_{i}"] = arrays_by_index[i]
        else:
            probe_dict[f"{variable_name}"] = df[column]
        
        processed_dict[column] = probe_dict

    return processed_dict

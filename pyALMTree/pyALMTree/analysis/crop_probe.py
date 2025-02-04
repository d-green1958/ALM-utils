import os
import numpy as np
import pandas as pd
import copy    


def crop_probe_data(
    probe_dict: dict, lower_limit: float = 0, upper_limit: float = 1e9
) -> dict:
    """
    Crops probe data dict by the time array according to lower_limit < t < upper_limit.

    Args:
        probe_dict (dict): Probe data dictionary
        lower_limit (float, optional): Lower cropping limit. Defaults to 0.
        upper_limit (float, optional): Upper cropping limit. Defaults to 1E9.

    Returns:
        dict: Cropped probe data dict.
    """

    # make a copy of the data
    cropped_probe_dict = copy.deepcopy(probe_dict)

    for key in cropped_probe_dict.keys():
        time = np.array(cropped_probe_dict[key]["time"])
        mask = (time > lower_limit) & (time < upper_limit)
        
        cropped_probe_dict[key]["time"] = time[mask]
        
        for probe_key in cropped_probe_dict[key]:
            if probe_key == "time":
                continue
            
            for value_key in cropped_probe_dict[key][probe_key].keys():
                if value_key in ["x", "y", "z"]:
                    continue
                cropped_probe_dict[key][probe_key][value_key] = np.array(cropped_probe_dict[key][probe_key][value_key])[mask]

            
            

    return cropped_probe_dict



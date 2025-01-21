import numpy as np

def crop_array_by_array(x_arr: np.ndarray, y_arrs: np.ndarray, lower_limit: float=0, upper_limit: float=1E9) -> tuple[np.ndarray, np.ndarray]:
    """
    Takes arrays stored in y_arrs and crops them according to the x_arr between the upper and lower limits.
    y_arrs will be returned with the indicies for which lower_limit<x_arr < upper_limit.

    Args:
        x_arr (np.ndarray): Array used to crop y_arrs.
        y_arrs (np.ndarray): Array of arrays to crop.
        lower_limit (float, optional): Upper limit. Defaults to 0.
        upper_limit (float, optional): Lower limit. Defaults to 1E9.

    Returns:
        np.ndarray: Cropped x_arr.
        np.ndarray: Array of cropped y_arrs.
    """
    cropped_arrs = np.zeros(len(y_arrs))
    crop_inds = [(x_arr > lower_limit) & (x_arr < upper_limit)]
    return x_arr[crop_inds] ,np.array(arr[crop_inds] for arr in y_arrs)
import numpy as np
from typing import Tuple


def phase_average_array(
    t_arr: np.ndarray,
    y_arrs: np.ndarray,
    frequency: float,
    phase_offset: float = 0,
    number_of_bins: int = 120,
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Phase averaged in input arrays stored within y_arrs using the times defined in t_arr.
    Note: y_arrs will contain many arrays so if you intend to only phase average a single
    array please pass this inside another array.

    Args:
        t_arr (np.ndarray): Array of times.
        y_arrs (np.ndarray): Array of arrays to phase average.
        frequency (float): Frequency to phase average given in Hz.
        phase_offset (float, optional): The phase when t=0. Defaults to 0.
        number_of_bins (int, optional): Number of bins. Defaults to 120.

    Returns:
        Tuple[np.ndarray, np.ndarray]: Array of bin midpoints (degrees), Phase averaged y_arrs
    """

    phase_arr = np.degrees(2*np.pi*frequency*t_arr + phase_offset)%360
    bins = np.linspace(0,360,number_of_bins)
    bin_inds = np.digitize(phase_arr, bins)
    bin_midpoints = (bins[1:] + bins[0:-1])*0.5
    
    phase_averaged_y_arrs = [[y_arr[bin_inds == i] for i in range(1,number_of_bins)] for y_arr in y_arrs]
    phase_averaged_y_arrs_std = np.array([[np.std(group) if len(group) > 0 else 0 for group in phase_averaged_y_arr] for phase_averaged_y_arr in phase_averaged_y_arrs])
    phase_averaged_y_arrs = np.array([[np.mean(group) if len(group) > 0 else 0 for group in phase_averaged_y_arr] for phase_averaged_y_arr in phase_averaged_y_arrs])


    return bin_midpoints, phase_averaged_y_arrs, phase_averaged_y_arrs_std
    
    
    

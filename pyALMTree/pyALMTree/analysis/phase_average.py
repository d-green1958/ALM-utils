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
        Tuple[np.ndarray, np.ndarray]: Array of bin centers (degrees), Phase averaged y_arrs
    """

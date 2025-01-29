import numpy as np
from typing import Tuple


def phase_average_array(
    t_arr: np.ndarray,
    y_arrs: np.ndarray,
    frequency: float,
    phase_offset: float = 0,
    number_of_bins: int = 120,
    bin_center_offset: float = 0,
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
        bin_center_offset (float, optional): Shifts the bin midpoints to the right (it must be positive). Default to 0.

    Returns:
        Tuple[np.ndarray, np.ndarray]: Array of bin midpoints (degrees), Phase averaged y_arrs
    """

    phase_arr = np.degrees(2 * np.pi * frequency * t_arr + phase_offset) % 360
    bins = np.linspace(0, 360, number_of_bins + 1)
    bin_midpoints = (bins[1:] + bins[0:-1]) * 0.5

    if bin_center_offset != 0:
        if bin_center_offset < 0:
            raise ValueError("Please use a positive bin_center_offset")
        elif bin_center_offset > 360.0 / (number_of_bins - 1):
            raise ValueError("bin_center_offset is larger than the bin width")
        else:
            # create the offset
            bins = bins + bin_center_offset
            bin_midpoints = (bin_midpoints + bin_center_offset) % 360

            # ensure the first and last values are 0 and 360
            bins = np.insert(bins, 0, 0)
            bins[-1] = 360

    bin_inds = np.digitize(phase_arr, bins)

    # note cant be a numpy array since non uniform lengths
    phase_averaged_y_arrs = [
        [y_arr[bin_inds == i] for i in range(1, number_of_bins + 2)] for y_arr in y_arrs
    ]

    if bin_center_offset != 0:
        for i in range(len(y_arrs)):

            # combine final array elements into last array
            phase_averaged_y_arrs[i][-1] = np.concatenate(
                (phase_averaged_y_arrs[i][0], phase_averaged_y_arrs[i][-1])
            )

            # remove first array from list
            phase_averaged_y_arrs[i] = phase_averaged_y_arrs[i][1:]

    phase_averaged_y_arrs_std = np.array(
        [
            [np.std(group) if len(group) > 0 else 0 for group in phase_averaged_y_arr]
            for phase_averaged_y_arr in phase_averaged_y_arrs
        ]
    )
    phase_averaged_y_arrs = np.array(
        [
            [np.mean(group) if len(group) > 0 else 0 for group in phase_averaged_y_arr]
            for phase_averaged_y_arr in phase_averaged_y_arrs
        ]
    )

    sorted_bin_midpoints_inds = np.argsort(bin_midpoints)
    bin_midpoints = bin_midpoints[sorted_bin_midpoints_inds]
    phase_averaged_y_arrs_std = phase_averaged_y_arrs_std[:, sorted_bin_midpoints_inds]
    phase_averaged_y_arrs = phase_averaged_y_arrs[:, sorted_bin_midpoints_inds]

    return bin_midpoints, phase_averaged_y_arrs, phase_averaged_y_arrs_std


if __name__ == "__main__":
    fs = 360  # Sampling frequency in Hz
    t = np.linspace(0, 10, 100*fs, endpoint=False)  # 1-second time vector
    signal = np.sin(2 * np.pi * 1 * t)  # 1 Hz sine wave
    noise = np.random.normal(0, 0.1, size=t.shape)  # Gaussian noise with std dev 0.1
    noisy_signal = signal + noise

    import matplotlib.pyplot as plt

    plt.plot(noisy_signal)

    plt.figure()
    bins, average, std = phase_average_array(
        t, [noisy_signal], frequency=1, number_of_bins=72, bin_center_offset=2.5
    )
    plt.plot(bins, average[0], marker="o")
    plt.show()

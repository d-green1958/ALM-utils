import numpy as np
from typing import Tuple
import copy


class PhaseAverageResult:
    def __init__(self):
        self.bin_midpoints = np.array([])
        self.phase_averaged_arrs = np.array([])
        self.phase_averaged_std_arrs = np.array([])
        self.bin_counts = np.array([])
        self.binned_values = np.array([])


def phase_average_array(
    t_arr: np.ndarray,
    y_arrs: np.ndarray,
    frequency: float,
    phase_offset: float = 0,
    number_of_bins: int = 45,
    bin_center_offset: float = None,
    include_0_and_360: bool = True,
    remove_phase_offset=False,
) -> PhaseAverageResult:
    """
    Phase averaged in input arrays stored within y_arrs using the times defined in t_arr.
    Note: y_arrs will contain many arrays so if you intend to only phase average a single
    array please pass this inside another array.

    Args:
        t_arr (np.ndarray): Array of times.
        y_arrs (np.ndarray): Array of arrays to phase average.
        frequency (float): Frequency to phase average given in Hz.
        phase_offset (float, optional): The phase when t=0. Defaults to 0.
        number_of_bins (int, optional): Number of bins. Defaults to 45.
        bin_center_offset (float, optional): Shifts the bin midpoints to the right (it must be positive). Default to half the bin width.
        include_0_and_360 (bool, optional): If 0 is a bin midpoint then the output arrays contain both 0 and 360 bins. Defaults to False.


    Returns:
        Tuple[np.ndarray, np.ndarray]: Array of bin midpoints (degrees), Phase averaged y_arrs
    """

    result = PhaseAverageResult()

    phase_arr = (np.degrees(2 * np.pi * frequency * t_arr) +
                 phase_offset) % 360
    bins = np.linspace(0, 360, number_of_bins + 1)
    bin_midpoints = (bins[1:] + bins[0:-1]) * 0.5

    if bin_center_offset == None:
        bin_center_offset = 180 / number_of_bins

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

    if remove_phase_offset:
        binned_y_arrs = []

        # first find phase angle
        fs = 1.0/np.mean(np.diff(t_arr))
        for ind, y_arr in enumerate(y_arrs):
            frequencies = np.fft.fftfreq(len(y_arr), 1/fs)
            fft_values = np.fft.fft(y_arr)
            index = np.argmax(np.abs(frequencies - frequency) < 1e-3)
            y_arr_phase = np.degrees(np.angle(fft_values[index])) + 90

            bin_inds = np.digitize(np.mod(phase_arr + y_arr_phase, 360), bins)

            # note cant be a numpy array since non uniform lengths
            binned_y_arrs.append([y_arr[bin_inds == i] for i in range(1, number_of_bins + 2)])

    else:
        bin_inds = np.digitize(phase_arr, bins)

        # note cant be a numpy array since non uniform lengths
        binned_y_arrs = [
            [y_arr[bin_inds == i] for i in range(1, number_of_bins + 2)] for y_arr in y_arrs
        ]

    if bin_center_offset != 0:
        for i in range(len(y_arrs)):

            # combine final array elements into last array
            binned_y_arrs[i][-1] = np.concatenate(
                (binned_y_arrs[i][0], binned_y_arrs[i][-1])
            )

            # remove first array from list
            binned_y_arrs[i] = binned_y_arrs[i][1:]

    phase_averaged_y_arrs_std = np.array(
        [
            [np.std(group) if len(group) > 0 else 0 for group in binned_y_arr]
            for binned_y_arr in binned_y_arrs
        ]
    )
    phase_averaged_y_arrs = np.array(
        [
            [np.mean(group) if len(group) > 0 else 0 for group in binned_y_arr]
            for binned_y_arr in binned_y_arrs
        ]
    )

    sorted_bin_midpoints_inds = np.argsort(bin_midpoints)
    bin_midpoints = bin_midpoints[sorted_bin_midpoints_inds]
    phase_averaged_y_arrs_std = phase_averaged_y_arrs_std[:,
                                                          sorted_bin_midpoints_inds]
    phase_averaged_y_arrs = phase_averaged_y_arrs[:, sorted_bin_midpoints_inds]

    if include_0_and_360:
        if 0 in bin_midpoints:
            bin_midpoints = np.append(bin_midpoints, 360)

            # Add a new column (axis=1) if phase_averaged_y_arrs is 2D
            phase_averaged_y_arrs = np.column_stack(
                (phase_averaged_y_arrs, phase_averaged_y_arrs[:, 0])
            )
            phase_averaged_y_arrs_std = np.column_stack(
                (phase_averaged_y_arrs_std, phase_averaged_y_arrs_std[:, 0])
            )

    result.bin_midpoints = np.array(bin_midpoints)
    result.binned_values = binned_y_arrs
    result.phase_averaged_arrs = np.array(phase_averaged_y_arrs)
    result.phase_averaged_std_arrs = np.array(phase_averaged_y_arrs_std)
    result.bin_counts = np.array(
        [[len(arr) for arr in binned_y_arr] for binned_y_arr in binned_y_arrs]
    )

    return result


if __name__ == "__main__":
    fs = 90*1000  # Sampling frequency in Hz
    t = np.linspace(0, 10,  fs, endpoint=False)  # 1-second time vector
    signal = np.sin(2 * np.pi * 1 * t + np.radians(180)) + np.sin(5 * np.pi * 1 * t + np.radians(189))   # 1 Hz sine wave
    # Gaussian noise with std dev 0.1
    noise = np.random.normal(0, 0.1, size=t.shape)
    noisy_signal = signal + noise

    import matplotlib.pyplot as plt

    plt.plot(noisy_signal)
    plt.grid()

    results = phase_average_array(
        t,
        [noisy_signal],
        frequency=1,
        remove_phase_offset=True
    )
    bins = results.bin_midpoints
    average = results.phase_averaged_arrs[0]
    bin_counts = results.bin_counts[0]
    std = results.phase_averaged_std_arrs[0]

    plt.figure()
    plt.plot(bins, average, marker="o")
    plt.fill_between(bins, average-std, average+std, color="b", alpha=0.3)
    plt.grid()
    plt.show()

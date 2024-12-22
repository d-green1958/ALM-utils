import matplotlib.pyplot as plt
import numpy as np
import os
from pyALMTree.read.turbineOutput import turbineOutput_file as read_file
import PyhD


def thrust(case_path, verbose=True):
    PyhD.matplotlib.style.apply_style()
    turbineOutput_path = os.path.join(case_path, "turbineOutput")
    turbineOutput_path = os.path.join(
        turbineOutput_path, os.listdir(turbineOutput_path)[0]
    )
    thrust_path = os.path.join(turbineOutput_path, "thrust")

    if not os.path.exists(thrust_path):
        FileNotFoundError("thrust file not found")

    if verbose:
        print(f"plotting thrust")

    df = read_file(thrust_path)
    figure, axs = PyhD.matplotlib.plot_helpers.landscape_fig(
        fig_name="Thrust",
        x_arrs=[df["Time(s)"]],
        y_arrs=[df["thrust (N)"]],
        x_label="Time [s]",
        y_label="Thrust [N]",
        title="Thrust Time Series",
    )

    return figure, axs


def thrust_FFT(case_path, verbose=True):
    PyhD.matplotlib.style.apply_style()
    turbineOutput_path = os.path.join(case_path, "turbineOutput")
    turbineOutput_path = os.path.join(
        turbineOutput_path, os.listdir(turbineOutput_path)[0]
    )
    thrust_path = os.path.join(turbineOutput_path, "thrust")

    if not os.path.exists(thrust_path):
        FileNotFoundError("thrust file not found")

    if verbose:
        print(f"plotting thrust FFT")

    df = read_file(thrust_path)

    timeseries = df["thrust (N)"]
    timevalues = df["Time(s)"]

    n = len(timeseries)

    timeseries_FT = np.fft.fft(timeseries)
    freqs = np.fft.fftfreq(n, d=timevalues[1] - timevalues[0])

    timeseries_FT = timeseries_FT[freqs >= 0]
    freqs = freqs[freqs >= 0]

    timeseries_FT = 2.0 * timeseries_FT / n

    figure, axs = PyhD.matplotlib.plot_helpers.landscape_fig(
        fig_name="Thrust FFT",
        x_arrs=[freqs, freqs],
        y_arrs=[np.real(timeseries_FT), np.imag(timeseries_FT)],
        label_arrs=["Real", "Imaginary"],
        x_label="Frequency [Hz]",
        y_label="Amplitude [N]",
        title="Thrust Spectral Content",
        legend=True,
    )

    return figure, axs


def thrust_FFT_log_log(case_path, verbose=True):
    PyhD.matplotlib.style.apply_style()
    turbineOutput_path = os.path.join(case_path, "turbineOutput")
    turbineOutput_path = os.path.join(
        turbineOutput_path, os.listdir(turbineOutput_path)[0]
    )
    thrust_path = os.path.join(turbineOutput_path, "thrust")

    if not os.path.exists(thrust_path):
        FileNotFoundError("thrust file not found")

    if verbose:
        print(f"plotting thrust FFT log-log")

    df = read_file(thrust_path)

    timeseries = df["thrust (N)"]
    timevalues = df["Time(s)"]

    n = len(timeseries)

    timeseries_FT = np.fft.fft(timeseries)
    freqs = np.fft.fftfreq(n, d=timevalues[1] - timevalues[0])

    timeseries_FT = timeseries_FT[freqs > 0]
    freqs = freqs[freqs > 0]

    timeseries_FT = 2.0 * timeseries_FT / n

    figure, axs = PyhD.matplotlib.plot_helpers.landscape_fig(
        fig_name="Thrust FFT log-log",
        x_arrs=[freqs, freqs],
        y_arrs=[np.real(timeseries_FT), np.imag(timeseries_FT)],
        label_arrs=["Real", "Imaginary"],
        x_label="Frequency [Hz]",
        y_label="Amplitude [N]",
        title="Thrust Spectral Content (log-log)",
        legend=True,
    )

    axs.set_xscale("log")
    axs.set_yscale("log")

    return figure, axs
import matplotlib.pyplot as plt
import numpy as np
import os
from pyALMTree.read.turbineOutput import turbineOutput_file as read_file
import PyhD


def thrust(case_path, time_series_limits=[0,1000], verbose=True, save_path=None):
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
    df = df[df["Time(s)"] >= time_series_limits[0]]
    df = df[df["Time(s)"] <= time_series_limits[1]]
    
    figure, axs = PyhD.matplotlib.plot_helpers.landscape_fig(
        fig_name="Thrust",
        x_arrs=[df["Time(s)"]],
        y_arrs=[df["thrust (N)"]],
        x_label="Time [s]",
        y_label="Thrust [N]",
        title="Thrust Time Series",
    )
    

    if not save_path == None:
        fig_path = os.path.join(save_path, "thrust")
        figure.savefig(fig_path, transparent=False)
        figure.savefig(fig_path + "_transparent", transparent=True)
        
    figure.tight_layout()

    return figure, axs


def thrust_FFT(case_path, time_series_limits=[0,1000], verbose=True, save_path=None):
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
    df = df[df["Time(s)"] >= time_series_limits[0]]
    df = df[df["Time(s)"] <= time_series_limits[1]]

    timeseries = np.array(df["thrust (N)"])
    timevalues = np.array(df["Time(s)"])

    n = len(timeseries)

    timeseries_FT = np.fft.fft(timeseries)
    freqs = np.fft.fftfreq(n, d=timevalues[1] - timevalues[0])

    timeseries_FT = timeseries_FT[freqs >= 0]
    freqs = freqs[freqs >= 0]

    timeseries_FT = 2.0 * np.abs(timeseries_FT) / n

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

    figure.tight_layout()
    
    if not save_path == None:
        fig_path = os.path.join(save_path, "thrust_FFT")
        figure.savefig(fig_path, transparent=False)
        figure.savefig(fig_path + "_transparent", transparent=True)
        

    return figure, axs

def thrust_details(case_path, time_series_limits=[0,1000], verbose=True, save_path=None):
    PyhD.matplotlib.style.apply_style()
    turbineOutput_path = os.path.join(case_path, "turbineOutput")
    turbineOutput_path = os.path.join(
        turbineOutput_path, os.listdir(turbineOutput_path)[0]
    )
    thrust_path = os.path.join(turbineOutput_path, "thrust")

    if not os.path.exists(thrust_path):
        FileNotFoundError("thrust file not found")

    if verbose:
        print(f"plotting thrust details")

    df = read_file(thrust_path)
    df = df[df["Time(s)"] >= time_series_limits[0]]
    df = df[df["Time(s)"] <= time_series_limits[1]]

    timeseries = np.array(df["thrust (N)"])
    timevalues = np.array(df["Time(s)"])
    
    n = len(timeseries)

    timeseries_FT = np.fft.fft(timeseries)
    freqs = np.fft.fftfreq(n, d=timevalues[1] - timevalues[0])

    timeseries_FT = timeseries_FT[freqs >= 0]
    freqs = freqs[freqs >= 0]

    timeseries_FT = 2.0 * np.abs(timeseries_FT) / n

    # figure, axs = plt.subplots()  # Adjust the size as needed
    figure = plt.figure(num="Thrust Details")
    axs = figure.gca()
    axs.axis('off')  
    
    column_labels = ["Parameter", "Value"]
    table_data = [
        ["Mean Value", f"{np.mean(df['thrust (N)']):.5g}"],
        ["Non-Zero Peak Location", f"{(freqs[freqs > 0])[np.argmax(timeseries_FT[freqs > 0])]:.5g}"],
        ["Non-Zero Peak Value", f"{np.real((timeseries_FT[freqs > 0])[np.argmax(timeseries_FT[freqs > 0])]):.5g}"],
        ["Non-Zero Peak-to-Peak Value", f"{2.0*np.real((timeseries_FT[freqs > 0])[np.argmax(timeseries_FT[freqs > 0])]):.5g}"]
    ]

    table = axs.table(
        cellText=table_data,  # Data for the cells
        colLabels=column_labels,  # Column headers
        loc='center',  # Center the table
        cellLoc='center'  # Center text within cells
    )

    figure.tight_layout()
    
    if not save_path == None:
        fig_path = os.path.join(save_path, "thrust_details")
        figure.savefig(fig_path, transparent=False)
        figure.savefig(fig_path + "_transparent", transparent=True)
        
    return figure, axs


def thrust_FFT_log_log(case_path, time_series_limits=[0,1000], verbose=True, save_path=None):
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
    df = df[df["Time(s)"] >= time_series_limits[0]]
    df = df[df["Time(s)"] <= time_series_limits[1]]

    timeseries = np.array(df["thrust (N)"])
    timevalues = np.array(df["Time(s)"])

    n = len(timeseries)

    timeseries_FT = np.fft.fft(timeseries)
    freqs = np.fft.fftfreq(n, d=timevalues[1] - timevalues[0])

    timeseries_FT = timeseries_FT[freqs > 0]
    freqs = freqs[freqs > 0]

    timeseries_FT = 2.0 * np.abs(timeseries_FT) / n

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
    
    figure.tight_layout()
    
    if not save_path == None:
        fig_path = os.path.join(save_path, "thrust_FFT_log_log")
        figure.savefig(fig_path, transparent=False)
        figure.savefig(fig_path + "_transparent", transparent=True)

    return figure, axs

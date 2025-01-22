import os
import numpy as np
from matplotlib.figure import Figure
from matplotlib.axes import Axes
from typing import List, Optional, Tuple
from pyALMTree.read.turbineOutput import turbineOutput_file as read_file
import PyhD

def alphaC(
    case_path: str,
    plot_time_targets: List[float] = [],
    verbose: bool = True,
    save_path: Optional[str] = None
) -> Tuple[Figure, Axes]:
    """
    Generates and plots the angle of attack (`alphaC`) as a function of radius for specified time targets.

    This function reads the angle of attack (`alphaC`) and radius (`radiusC`) data from a simulation case,
    extracts the data corresponding to the specified time targets, and creates a plot. Optionally, the plot
    can be saved to the specified path.

    Args:
        case_path (str): Path to the root directory of the simulation case. The function assumes the data 
                         is located in the `turbineOutput` subdirectory.
        plot_time_targets (List[float], optional): List of target times (in seconds) for which to extract and 
                                                   plot the angle of attack. Defaults to an empty list.
        verbose (bool, optional): If True, prints progress messages. Defaults to True.
        save_path (Optional[str], optional): Path to save the generated plot. If None, the plot will not be saved. 
                                             Defaults to None.

    Raises:
        FileNotFoundError: If the required `alphaC` or `radiusC` file is not found in the expected directory.

    Returns:
        Tuple[Figure, Axes]: A tuple containing:
            - `figure` (matplotlib.figure.Figure): The generated plot figure.
            - `axs` (matplotlib.axes._axes.Axes): The axes object of the generated plot.

    Example:
        >>> figure, axs = alphaC("/path/to/case", plot_time_targets=[0.5, 1.0, 1.5], save_path="./plots")
    """
    PyhD.matplotlib.style.apply_style()
    turbineOutput_path = os.path.join(case_path, "turbineOutput")
    turbineOutput_path = os.path.join(
        turbineOutput_path, os.listdir(turbineOutput_path)[0]
    )
    alpha_path = os.path.join(turbineOutput_path, "alphaC")
    radius_path = os.path.join(turbineOutput_path, "radiusC")

    if not os.path.exists(alpha_path):
        raise FileNotFoundError("alpha file not found")
    if not os.path.exists(radius_path):
        raise FileNotFoundError("radiusC file not found")

    if verbose:
        print(f"plotting alpha")

    df = read_file(alpha_path, blade_data_file=True)
    df_radius = read_file(radius_path, blade_data_file=True)
    radius = np.array(df_radius[df_radius["Blade"] == 0]["radiusC(m)"][0])
        
    alpha_arr = []
    radius_arr = []
    plot_times_arr = []
        
    for ind, target_time in enumerate(plot_time_targets):        
        row_index = np.argmin(np.abs(df["Time(s)"] - target_time))  
        row_time_value = df["Time(s)"][row_index]
        alpha_arr.append(df["angle-of-attack(degrees)"][row_index])
        radius_arr.append(radius)
        plot_times_arr.append(row_time_value)
    
    figure, axs = PyhD.matplotlib.plot_helpers.landscape_fig(
        fig_name="alpha",
        x_arrs=radius_arr,
        y_arrs=alpha_arr,
        label_arrs=plot_times_arr,
        legend=True,
        legend_title="Time [s]",
        x_label="Radius [m]",
        y_label=r"Angle of Attack [$^\circ$]",
        title="Angle of Attack",
        markerstyle_arrs = np.full(len(radius_arr), ".")
    )
    

    if save_path is not None:
        fig_path = os.path.join(save_path, "alphaC")
        figure.savefig(fig_path, transparent=False)
        figure.savefig(fig_path + "_transparent", transparent=True)
        
    figure.tight_layout()
    return figure, axs

    
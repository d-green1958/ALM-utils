import matplotlib.pyplot as plt
import numpy as np
import os
from pyALMTree.read.turbineOutput import turbineOutput_file as read_file
import PyhD

def tangentialForce(case_path, plot_time_targets=[], verbose=True, save_path=None):
    PyhD.matplotlib.style.apply_style()
    turbineOutput_path = os.path.join(case_path, "turbineOutput")
    turbineOutput_path = os.path.join(
        turbineOutput_path, os.listdir(turbineOutput_path)[0]
    )
    tangentialForce_path = os.path.join(turbineOutput_path, "tangentialForce")
    radius_path = os.path.join(turbineOutput_path, "radiusC")

    if not os.path.exists(tangentialForce_path):
        FileNotFoundError("tangentialForce file not found")
    if not os.path.exists(radius_path):
        FileNotFoundError("radiusC file not found")

    if verbose:
        print(f"plotting tangentialForce")

    df = read_file(tangentialForce_path, blade_data_file=True)
    df_radius = read_file(radius_path, blade_data_file=True)
    radius = np.array(df_radius[df_radius["Blade"] == 0]["radiusC(m)"][0])
        
    tangentialForce_arr = []
    radius_arr = []
    plot_times_arr = []
        
    for ind, target_time in enumerate(plot_time_targets):        
        row_index = np.argmin(np.abs(df["Time(s)"] - target_time))  
        row_time_value = df["Time(s)"][row_index]
        tangentialForce_arr.append(df["tangential force (N)"][row_index])
        radius_arr.append(radius)
        plot_times_arr.append(row_time_value)
    
    figure, axs = PyhD.matplotlib.plot_helpers.landscape_fig(
        fig_name="tangentialForce",
        x_arrs=radius_arr,
        y_arrs=tangentialForce_arr,
        label_arrs=plot_times_arr,
        legend=True,
        legend_title="Time [s]",
        x_label="Radius [m]",
        y_label=r"Axial Force [N]",
        title="Tangential Force",
        markerstyle_arrs = np.full(len(radius_arr), ".")
    )
    
    if not save_path == None:
        fig_path = os.path.join(save_path, "tangentialForce")
        figure.savefig(fig_path, transparent=False)
        figure.savefig(fig_path + "_transparent", transparent=True)
        
    figure.tight_layout()
    return figure, axs
    
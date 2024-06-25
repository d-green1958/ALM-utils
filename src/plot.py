import matplotlib.pyplot as plt
import numpy as np
import sys

def plot_power_and_thrust_time_series(data, start_time = None, end_time = None):
    keys = ["powerRotor","thrust","times"]
    for key in keys:
        if key not in data.keys():
            print(f"{key} not in data")
            sys.exit(1)
    
    power = data["powerRotor"]
    thrust = data["thrust"]
    times = data["times"]
    
    fig, ax1 = plt.subplots()

    ax1.plot(times, power, 'b-', label='power')
    ax1.set_xlabel('time s')
    ax1.set_ylabel('Power W', color='b')
    ax1.tick_params(axis='y', labelcolor='b')

    ax2 = ax1.twinx()
    ax2.plot(times, thrust, 'r-', label='torque')
    ax2.set_ylabel('Thrust N', color='r')
    ax2.tick_params(axis='y', labelcolor='r')

    fig.tight_layout()
    ax1.legend(loc='upper left')
    ax2.legend(loc='upper right')
    ax1.grid(True)
    
    print("plotting power and torque time series")
    
    
    
def plot_instantaneous_spanwise_forces(radial_pos, times, forces, plot_time):
    number_of_keys = len(forces.keys())
    if "times" in forces.keys():
        number_of_keys -= 1
    
    # find the index of the target time
    difs = times - [plot_time]*len(times)
    abs_difs = abs(difs)
    min_value = min(abs_difs)
    inds = [i for i, x in enumerate(abs_difs) if x == min_value]
    time_index = inds[0]
    nearest_time = times[inds[0]]
    if nearest_time != plot_time:
        print(f'trying to plot at {plot_time}s', end= ' ')
        print(f'--> nearest time is {times[time_index]}s [timestep: {time_index}]')
        plot_time = nearest_time
    else:
        print(f"plotting at time {plot_time}s")
    
    # normalise the radial distances
    num_points = len(radial_pos)
    radial_pos = [float(val) for val in radial_pos]
    max_rad = max(radial_pos)
    radial_pos_normalised = [((val)/max_rad) for val in radial_pos] 
    
    # find distances between points
    element_length = np.zeros(num_points)
    element_length[0] = radial_pos[1]-radial_pos[0]
    element_length[-1] = radial_pos[-1]-radial_pos[-2]
    for index, elem in enumerate(radial_pos):
        if (index>=1 and index < num_points-1):
            element_length[index] = (radial_pos[index+1]-radial_pos[index])
    
    
    # create the subplots
    fig, axs = plt.subplots(1,number_of_keys)
    plot_counter = 0
    
    for key in forces.keys():
        if key == "times":
            continue
        force_data = forces[key]
        for blade_id in range(len(force_data)):
            force = force_data[blade_id][time_index]
            
            force_per_length = force/element_length            
            axs[plot_counter].plot(radial_pos_normalised, force_per_length, label=f"blade {blade_id}")
            
        axs[plot_counter].set_title(key)
        axs[plot_counter].grid(True)
        axs[plot_counter].set_ylabel("Force [N]")
        axs[plot_counter].set_xlabel("r/R")
        axs[plot_counter].legend()
            
        plot_counter += 1
    
    fig.suptitle(f"Spanwise forces at t={plot_time}s")
    fig.tight_layout()

    
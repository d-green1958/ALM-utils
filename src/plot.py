import matplotlib.pyplot as plt
import numpy as np
import sys
from .analysis import find_nearest_time

def plot_power_and_thrust_time_series(data, start_time = None, end_time = None):
    keys = ["powerRotor","thrust","times"]
    for key in keys:
        if key not in data.keys():
            print(f"{key} not in data")
            sys.exit(1)
    
    power = data["powerRotor"]
    thrust = data["thrust"]
    times = data["times"]
    
    if start_time == None:
        print(f"plotting time series from {times[0]}")
    else:
        inds, nearest_time = find_nearest_time(start_time, times)
        print(f"plotting time series from {nearest_time}")
        start_ind = inds[0]
        times = times[start_ind:]
        power = power[start_ind:]
        thrust = thrust[start_ind:]
    
    
    if end_time == None:
        print(f"plotting time series until {times[-1]}")
    else:
        inds, nearest_time = find_nearest_time(end_time, times)
        print(f"plotting time series until {nearest_time}")
        end_ind = inds[0]
        times = times[:end_ind]
        power = power[:end_ind]
        thrust = thrust[:end_ind]
        
    
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
    
    # round to the nearest time
    inds, nearest_time = find_nearest_time(plot_time, times)
    time_index = inds[0]
    
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
    
def plot_power_and_thrust_convergence(data, start_time = None, end_time = None, rotor_time_period = None):
    fig, ax1 = plt.subplots()
    
    
    power = data["powerRotor"]
    thrust = data["thrust"]
    times = data["times"]
    
    if start_time == None:
        print(f"plotting time series from {times[0]}")
    else:
        inds, nearest_time = find_nearest_time(start_time, times)
        print(f"plotting time series from {nearest_time}")
        start_ind = inds[0]
        times = times[start_ind:]
        power = power[start_ind:]
        thrust = thrust[start_ind:]
            
    
    if end_time == None:
        print(f"plotting time series until {times[-1]}")
    else:
        inds, nearest_time = find_nearest_time(end_time, times)
        print(f"plotting time series until {nearest_time}")
        end_ind = inds[0]
        times = times[:end_ind]
        power = power[:end_ind]
        thrust = thrust[:end_ind]     
    
    power_final = power[-1]
    thrust_final = thrust[-1]
    
    
    power_residual = np.abs((power - power_final)/power_final)
    thrust_residual = np.abs((thrust - thrust_final)/thrust_final)
    
    ax1.plot(times, power_residual, label = "power")
    ax1.plot(times, thrust_residual, label = "thrust")
    ax1.set_yscale("log")
    ax1.set_ylabel(r"$\frac{\Delta q}{q}$")
    ax1.set_xlabel("time s")
    ax1.legend()
    ax1.grid(True)
    
    ax2 = ax1.twiny()
    ax2.set_xlim(ax1.get_xlim())

    nondimensional_times = times/rotor_time_period
    num_periods = (end_time-start_time)/rotor_time_period
    num_ticks =  int(num_periods*4) # Number of desired ticks
    tick_indices = np.linspace(0, len(times) - 1, num_ticks, dtype=int)
    ax2.set_xticks(times[tick_indices])
    formatted_labels = [f"{x:.2f}" for x in nondimensional_times[tick_indices]]
    ax2.set_xticklabels(formatted_labels)

    ax2.set_xlabel('t/T')

    plt.title('Power and Torque Convergence')
    plt.tight_layout()
        

    
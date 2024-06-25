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
    
    
    
    

    
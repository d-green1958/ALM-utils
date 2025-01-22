import numpy as np

def find_cropped_mean(x_arr, y_arr, x_lims):
    y_arr = np.array(y_arr)
    x_arr = np.array(x_arr)
    
    cropped_y = y_arr[np.where((x_arr > x_lims[0]) & (x_arr < x_lims[1]))[0]]
    return np.mean(cropped_y)
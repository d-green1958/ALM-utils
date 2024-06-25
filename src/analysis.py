import numpy as np

def find_nearest_time(target_time, times):
    # find the index of the target time
    difs = times - [target_time]*len(times)
    abs_difs = np.abs(difs)
    min_value = min(abs_difs)
    inds = [i for i, x in enumerate(abs_difs) if x == min_value]
    time_index = inds[0]
    nearest_time = times[inds[0]]
    
    return inds, nearest_time
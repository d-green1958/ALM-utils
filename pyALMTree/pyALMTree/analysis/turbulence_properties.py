import numpy as np


class TurbulenceResult:
    def __init__(self):
        self.k = None
        self.L = np.zeros((3, 3))
        self.T = np.zeros((3, 3))
        self.U_mean = np.zeros(3)
        self.R = np.zeros((3, 3))

def calculate_T(U_fluc_arr, V_fluc_arr, t_arr):
    def R(u, v):
        return np.mean((u * v)) / np.mean(u * u)
    num_time_steps = len(U_fluc_arr)
    ref_time_ind = num_time_steps // 2

    tau_arr = np.arange(
        ref_time_ind - num_time_steps + 1, num_time_steps - ref_time_ind - 1
    )
    R_arr = np.zeros_like(tau_arr, dtype=float)

    for ind, tau in enumerate(tau_arr):
        if tau >= 0:
            R_arr[ind] = R(
                U_fluc_arr[ref_time_ind:0:-1],
                V_fluc_arr[ref_time_ind + tau : tau : -1],
            )
        elif tau < 0:
            R_arr[ind] = R(
                U_fluc_arr[ref_time_ind:num_time_steps],
                V_fluc_arr[ref_time_ind + tau : num_time_steps + tau],
            )
        else:
            raise ValueError("tau is misbehaving")

    zero_crossings = np.where(np.diff(np.sign(R_arr)))[0]
    zero_crossings = np.append(zero_crossings, num_time_steps)
    zero_crossings = np.append(zero_crossings, 0)

    upper = np.min(zero_crossings[zero_crossings >= ref_time_ind])
    lower = np.max(zero_crossings[zero_crossings <= ref_time_ind])

    dt = t_arr[lower + 1] - t_arr[lower]
    T = np.sum(R_arr[lower:upper] * dt)
    return T


def calculate_turbulence_properties(
    t_arr: np.ndarray, U_arr: np.ndarray, t_limits: np.ndarray = [0,1000],
) -> TurbulenceResult:
    """
    Calculate k,L,T,R,U_mean and store it in a result output

    Args:
        t_arr (np.ndarray): Array of time values.
        U_arr (np.ndarray): Array of (U,V,W) where U,V,W and the velocity time series signals.
        t_limits (np.ndarray): Array containing the limits of the analysis (i.e. [t_lower_limit, t_upper_limiit]). Defaults to [0,1000].

    Returns:
        TurbulenceResult: Results (k,L,T,U_mean,R)
    """
    result = TurbulenceResult()
    
    from .crop_arrays import crop_array_by_array
    t_arr_cropped, U_arr_cropped = crop_array_by_array(t_arr, U_arr, t_limits[0], t_limits[1])
    t_arr = t_arr_cropped
    U_arr = U_arr_cropped

    # Mean velocity
    U_mean = np.mean(U_arr, axis=1)
    result.U_mean = U_mean

    # Reynolds Stresses (Resolved)
    U_fluc_arr = U_arr - U_mean[:, np.newaxis]
    R = np.zeros((3, 3))
    for i in range(3):
        for j in range(3):
            R[i, j] = np.mean(U_fluc_arr[i] * U_fluc_arr[j])
    result.R = R

    # TKE
    k = 0.5 * np.trace(R)
    result.k = k

    # Calculate timescale
    N = len(U_fluc_arr[0])
    for i in range(3):
        for j in range(3):
            T = calculate_T(U_fluc_arr[i], U_fluc_arr[j], t_arr)
            result.T[i,j] = T

    return result

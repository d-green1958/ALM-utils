import numpy as np


class TurbulenceResult:
    def __init__(self):
        self.k = None
        self.L = np.zeros((3, 3))
        self.T = np.zeros((3, 3))
        self.U_mean = np.zeros(3)
        self.R = np.zeros((3, 3))


def calculate_turbulence_properties(
    t_arr: np.ndarray, U_arr: np.ndarray
) -> TurbulenceResult:
    """
    Calculate k,L,T,R,U_mean and store it in a result output

    Args:
        t_arr (np.ndarray): Array of time values.
        U_arr (np.ndarray): Array of (U,V,W) where U,V,W and the velocity time series signals.

    Returns:
        TurbulenceResult: Results (k,L,T,U_mean,R)
    """
    result = TurbulenceResult()

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
            autocorrelation = (
                np.correlate(U_fluc_arr[i], U_fluc_arr[j], mode="full")
                / np.sqrt(np.var(U_fluc_arr[i]) * np.var(U_fluc_arr[j]))
                / N
            )
            autocorrelation = autocorrelation[N - 1 :]

            delta_tau = np.mean(np.diff(t_arr))
            dtau = np.arange(0, len(autocorrelation)) * delta_tau
            T = np.trapz(autocorrelation, dtau)
            result.T[i,j] = T
            
    return result

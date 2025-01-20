def find_peak_to_peak(y_arr, t_arr, frequency, cut_time):

    y_arr = np.array(y_arr)
    t_arr = np.array(t_arr)

    y_arr = y_arr[t_arr > cut_time]
    t_arr = t_arr[t_arr > cut_time]

    fs = 1.0 / (t_arr[1] - t_arr[0])
    n = len(t_arr)

    y_arr_FT = np.fft.fft(y_arr)
    freq = np.fft.fftfreq(n, d=t_arr[1] - t_arr[0])

    index = np.argmin(np.abs(freq - frequency))
    return 4.0 / n * np.abs(y_arr_FT[index])

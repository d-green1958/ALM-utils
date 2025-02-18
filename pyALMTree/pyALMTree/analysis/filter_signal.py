def low_pass_filter_arr(y_arr, cutoff, fs):
    import numpy as np
    fft_signal = np.fft.fft(y_arr)
    freqs = np.fft.fftfreq(len(y_arr), 1/fs)  
    mask = (freqs <= cutoff) & (freqs >= -cutoff)
    fft_signal_filtered = fft_signal * mask
    filtered_signal = np.fft.ifft(fft_signal_filtered)
    return np.real(filtered_signal)
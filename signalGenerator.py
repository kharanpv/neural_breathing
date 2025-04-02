import numpy as np 

def signalGenerator(TotalTime, signal_period):
    """
    Python version of signalGenerator.m
    Generates a sequence of signals with given period
    
    Args:
        TotalTime: Length of output signal
        signal_period: Spacing between 1s in the signal
        
    Returns:
        c: numpy array of shape (TotalTime,) with periodic 1s
    """
    c = np.zeros(TotalTime)
    num = TotalTime // signal_period
    
    # Randomize the starting point (MATLAB: floor(signal_period*rand)+1)
    k = np.random.randint(1, signal_period+1)
    
    for i in range(num + 1):
        idx = i * signal_period + k - 1  # -1 for 0-based indexing
        if idx < TotalTime:
            c[idx] = 1
    
    return c
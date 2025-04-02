import numpy as np

def parameters_phase3_paperC():
    """
    Python implementation of parameters_phase3_paperC.m
    Returns parameter vectors for the 3-node network in phase 3 configuration.
    
    Returns:
        params1, params3, params4: Parameter vectors for each node
    """
    # Parameters for cell 1
    m1 = 100                # Memory reset threshold when x1 is active
    memoryLen1 = 400        # Total memory length for cell 1
    n_pos1 = 2              # Nodes in self-excitation loop (including x1)
    activeThreshold1 = 2    # Activators needed to activate x1
    signal_period1 = 5      # Control signal period for c1
    
    # Parameters for cell 3
    memoryLen3 = 400
    activeThreshold3 = 2
    signal_period3 = 110    # Period of C3
    m3 = 100
    n_pos3 = 2              # Note: Uses same n_pos as cell 1 in MATLAB
    
    # Parameters for cell 4 (phase3-specific)
    memoryLen4 = 800
    activeThreshold4 = 3
    signal_period4 = 32     # Key difference in phase3 (vs 350 in phase2)
    m4 = memoryLen4         # All memories reset when x4 is active
    
    # Create parameter vectors (MATLAB-like 1-based indexing simulation)
    params1 = np.zeros(5, dtype=int)
    params1[0] = m1            # params1(1) in MATLAB
    params1[1] = memoryLen1    # params1(2)
    params1[2] = n_pos1        # params1(3)
    params1[3] = activeThreshold1  # params1(4)
    params1[4] = signal_period1    # params1(5)
    
    params3 = np.zeros(5, dtype=int)
    params3[0] = memoryLen3    # params3(1)
    params3[1] = activeThreshold3  # params3(2)
    params3[2] = signal_period3    # params3(3)
    params3[3] = m3            # params3(4)
    params3[4] = n_pos3        # params3(5)
    
    params4 = np.zeros(4, dtype=int)
    params4[0] = memoryLen4    # params4(1)
    params4[1] = activeThreshold4  # params4(2)
    params4[2] = signal_period4    # params4(3)
    params4[3] = m4            # params4(4)
    
    return params1, params3, params4

if __name__ == "__main__":
    # Test parameter loading
    p1, p3, p4 = parameters_phase3_paperC()
    print("Cell 1 params:", p1)
    print("Cell 3 params:", p3)
    print("Cell 4 params:", p4)
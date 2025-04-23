import numpy as np

def parameters_phase1_paperC():
    """
    Python implementation of parameters_phase1_paperC.m
    Returns parameter vectors for the 3-node network in phase 1 configuration.
    
    Returns:
        params1, params3, params4: Parameter vectors for each node
    """
    # Parameters for cell 1 (phase 1 specific)
    m1 = 100                # Memory reset threshold when x1 is active
    memoryLen1 = 400        # Total memory length for cell 1
    n_pos1 = 2              # Nodes in self-excitation loop (including x1)
    activeThreshold1 = 2    # Activators needed to activate x1
    signal_period1 = 110    # Control signal period for c1 (phase1 value)
    
    # Parameters for cell 3 (phase 1 specific)
    memoryLen3 = 400
    activeThreshold3 = 2
    signal_period3 = 500    # Period of C3 (phase1 value)
    m3 = 100
    n_pos3 = 2              # Note: Uses same n_pos as cell 1 in MATLAB
    
    # Parameters for cell 4 (phase 1 specific)
    memoryLen4 = 800
    activeThreshold4 = 3
    signal_period4 = 1000   # Period of C4 (phase1 value)
    m4 = memoryLen4         # All memories reset when x4 is active
    
    # Create parameter vectors
    params1 = np.zeros(5)
    params1[0] = m1            # params1(1)
    params1[1] = memoryLen1    # params1(2)
    params1[2] = n_pos1        # params1(3)
    params1[3] = activeThreshold1  # params1(4)
    params1[4] = signal_period1    # params1(5)
    
    params3 = np.zeros(5)
    params3[0] = memoryLen3    # params3(1)
    params3[1] = activeThreshold3  # params3(2)
    params3[2] = signal_period3    # params3(3)
    params3[3] = m3            # params3(4)
    params3[4] = n_pos3        # params3(5)
    
    params4 = np.zeros(4)
    params4[0] = memoryLen4    # params4(1)
    params4[1] = activeThreshold4  # params4(2)
    params4[2] = signal_period4    # params4(3)
    params4[3] = m4            # params4(4)
    
    return params1, params3, params4

if __name__ == "__main__":
    # Test parameter loading
    p1, p3, p4 = parameters_phase1_paperC()
    print("=== Phase 1 Parameters ===")
    print("Cell 1 params:", p1)
    print("Cell 3 params:", p3)
    print("Cell 4 params:", p4)
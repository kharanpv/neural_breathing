import numpy as np

def f3_A(currentState, control, params3):
    """
    Python version of f3_A.m - governing function for node x3 and its signals
    
    Args:
        currentState: Current state vector (numpy array)
        control: Control signal (0 or 1)
        params3: Parameter vector [memoryLen3, activeThreshold, signal_period3, m, n_pos]
        
    Returns:
        nextState: Updated state vector
    """
    len_state = len(currentState)
    nextState = np.zeros(len_state)
    
    # Unpack parameters (note Python 0-based indexing)
    activeThreshold = params3[1]  # params3(2) in MATLAB
    n_pos = params3[4]           # params3(5) in MATLAB
    m = params3[3]               # params3(4) in MATLAB
    
    # Update x3 (first element)
    sumActivator_x = np.sum(currentState[n_pos-1:])  # n_pos-1 for Python indexing
    if sumActivator_x >= activeThreshold:
        nextState[0] = 1
    
    # Update inner loop nodes (shift register)
    for k in range(1, n_pos):
        nextState[k] = currentState[k-1]
    
    # Update memory chain nodes
    currentS = currentState[n_pos:]
    lenS = len(currentS)
    nextS = np.zeros(lenS)
    
    # First memory element
    nextS[0] = control
    
    # Remaining memory elements (simple shift)
    for k in range(1, lenS):
        nextS[k] = currentS[k-1]
    
    # Memory erase when x3 is active
    if currentState[0] > 0:
        for k in range(m, lenS):  # m is 1-based length in MATLAB
            nextS[k] = 0
    
    # Combine memory updates with other states
    nextState[n_pos:] = nextS
    
    return nextState
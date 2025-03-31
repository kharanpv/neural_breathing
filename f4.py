import numpy as np

def f4(currentState, x3, control, params4):
    """
    Python version of f4.m - governing function for node x4 and its signals
    
    Args:
        currentState: Current state vector (numpy array)
        x3: Input from node 3 (0 or 1, acts as inhibitor)
        control: Control signal (0 or 1)
        params4: Parameter vector [memoryLen4, activeThreshold, signal_period4, m]
        
    Returns:
        nextState: Updated state vector
    """
    len_state = len(currentState)
    nextState = np.zeros(len_state)
    
    # Unpack parameters (note Python 0-based indexing)
    activeThreshold = params4[1]  # params4(2) in MATLAB
    m = params4[3]               # params4(4) in MATLAB
    
    # Update x4 (first element)
    sumActivator_x = np.sum(currentState[1:])  # Sum all except first element
    if sumActivator_x >= activeThreshold:
        nextState[0] = 1
    
    # Update memory chain nodes
    currentS = currentState[1:]
    lenS = len(currentS)
    nextS = np.zeros(lenS)
    
    # First memory element
    nextS[0] = control * (1 - x3)  # x3 acts as inhibitor
    
    # Remaining memory elements
    for k in range(1, lenS):
        nextS[k] = currentS[k-1] * (1 - x3)
    
    # Memory erase when x4 is active (currentState[0] > 0)
    if currentState[0] > 0:
        for k in range(m, lenS):  # m is 1-based length in MATLAB
            nextS[k] = 0
    
    # Combine memory updates with x4 state
    nextState[1:] = nextS
    
    return nextState
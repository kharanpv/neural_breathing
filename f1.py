import numpy as np

def f1(currentState, x3, x4, control, params1):
    """
    Python version of f1.m - governing function for node x1 and its signals
    
    Args:
        currentState: Current state vector (numpy array)
        x3, x4: Inputs from other nodes (0 or 1)
        control: Control signal (0 or 1)
        params1: Parameter vector [m1, memoryLen1, n_pos1, activeThreshold]
        
    Returns:
        nextState: Updated state vector
    """
    len_state = len(currentState)
    nextState = np.zeros(len_state)
    
    # Unpack parameters (note Python 0-based indexing)
    activeThreshold = params1[3]  # params1(4) in MATLAB
    n_pos = params1[2]           # params1(3) in MATLAB
    m1 = params1[0]              # params1(1) in MATLAB
    
    # Update x1 (first element)
    sumActivator_x1 = np.sum(currentState[n_pos-1:])  # n_pos-1 for Python indexing
    if sumActivator_x1 >= activeThreshold:  # Original had: && (x4==0) if needed
        nextState[0] = 1  # x1 position
    
    # Update nodes in excitatory loop (shift register)
    for k in range(1, n_pos):
        nextState[k] = currentState[k-1]
    
    # Update memory chain nodes
    currentS = currentState[n_pos:]
    lenS = len(currentS)
    nextS = np.zeros(lenS)
    
    # First memory element
    nextS[0] = control * (1 - x3) * (1 - x4)  # x3/x4 act as inhibitors
    
    # Remaining memory elements
    for k in range(1, lenS):
        nextS[k] = currentS[k-1] * (1 - x3) * (1 - x4)
    
    # Zero out memories beyond m1 if x1 is active
    if currentState[0] > 0:
        for k in range(m1, lenS):  # m1 is 1-based length in MATLAB
            nextS[k] = 0
    
    # Combine memory updates with other states
    nextState[n_pos:] = nextS
    
    return nextState
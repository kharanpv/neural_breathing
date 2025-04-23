import numpy as np

def findPattern(x, pattern):
    """
    Python version of findPattern.m - locates all occurrences of a pattern in a vector.
    
    Args:
        x: Input vector (NumPy array)
        pattern: Pattern to search for (NumPy array)
        
    Returns:
        starts: Indices where pattern begins (1-based like MATLAB)
    """
    pat_len = len(pattern)
    x_len = len(x)
    
    if pat_len == 0 or x_len < pat_len:
        return np.array([])
    
    # Pre-allocate (MATLAB's Max_num = floor(x_len/pat_len))
    max_num = x_len // pat_len
    starts = np.zeros(max_num, dtype=int)
    
    k = 0  # Match counter
    n = 0  # Current position (0-based)
    
    while n <= x_len - pat_len:
        # Compare slices (vectorized for speed)
        if np.array_equal(x[n:n+pat_len], pattern):
            starts[k] = n + 1  # Convert to 1-based indexing
            k += 1
            n += pat_len  # Skip ahead after match
        else:
            n += 1
    
    # Trim unused pre-allocation
    return starts[:k] if k > 0 else np.array([])
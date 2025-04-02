import numpy as np
from scipy.io import savemat
import matplotlib.pyplot as plt
from import_handler import get_function_or_fallback 

# Import relevant functions from other files (with error handling)
parameters_phase2_paperC = get_function_or_fallback("parameters_phase2_paperC")
TrajectoryGenerator_3Nodes = get_function_or_fallback("TrajectoryGenerator_3Nodes")
findPattern = get_function_or_fallback("findPattern")

def Varying_c1_phase2():
    """Python version of Varying_c1_phase2.m"""
    # Clear workspace equivalent (not needed in Python)
    
    # Load parameters (placeholder)
    params1, params3, params4 = parameters_phase2_paperC()  # TODO: Implement this
    
    TotalTime = 6000
    startPeriod = 1
    endPeriod = 56
    step_period = 5
    num_period = int((endPeriod - startPeriod) / step_period)
    
    # Initialize data structure
    class DataStruct:
        def __init__(self):
            self.signal_period = 0
            self.expiration = []
            self.inspiration = []
            self.totalBreath = []
    
    Data_inp_exp = []
    numData = 0
    
    # Main loop
    for k in range(num_period):
        signal_period = startPeriod + step_period * k
        params1[4] = signal_period  # Python uses 0-based indexing (original: params1(5))
        totT = TotalTime + 2 * signal_period
        
        for i in range(10):
            # Generate trajectories (placeholder)
            Net1, Net3, Net4 = TrajectoryGenerator_3Nodes(totT, params1, params3, params4)
            
            # Plotting (optional)
            node1 = Net1[:, 0]
            node3 = Net3[:, 0]
            node4 = Net4[:, 0]
            
            plt.figure(1)
            plt.clf()
            
            plt.subplot(2, 2, 1)
            plt.plot(node1, '*')
            plt.ylabel('x1')
            
            plt.subplot(2, 2, 2)
            plt.plot(node3, '*')
            plt.ylabel('x3')
            
            plt.subplot(2, 2, 3)
            plt.plot(node4, '*')
            plt.ylabel('x4')
            
            # Pattern detection (placeholder)
            starts = findPattern(node1, np.array([0, 1]))
            ends = findPattern(node1, np.array([1, 0]))
            len_starts = len(starts)
            len_ends = len(ends)
            
            if len_starts > 3:
                starts = starts[1:]
                ends = ends[1:]
                minLen = min(len(starts), len(ends))
                
                if starts[0] < ends[0]:
                    number_1s = ends[:minLen] - starts[:minLen]
                    number_0s = starts[1:minLen] - ends[:minLen-1]
                else:
                    number_1s = ends[1:minLen] - starts[:minLen-1]
                    number_0s = starts[:minLen] - ends[:minLen]
                
                numData += 1
                data = DataStruct()
                data.expiration = number_0s
                data.inspiration = number_1s
                data.totalBreath = starts[1:len_starts-1] - starts[:len_starts-2]
                data.signal_period = signal_period
                Data_inp_exp.append(data)
            else:
                print('Trajectory is not long enough, please increase TotalTime')
    
    # Convert to matrix format
    All_data = np.zeros((80000, 3))
    count = 0
    
    for j in range(numData):
        # Expiration data
        len0 = len(Data_inp_exp[j].expiration)
        sg = Data_inp_exp[j].signal_period
        All_data[count:count+len0, :2] = np.tile([sg, 0], (len0, 1))
        All_data[count:count+len0, 2] = Data_inp_exp[j].expiration
        count += len0
        
        # Inspiration data
        len1 = len(Data_inp_exp[j].inspiration)
        All_data[count:count+len1, :2] = np.tile([sg, 1], (len1, 1))
        All_data[count:count+len1, 2] = Data_inp_exp[j].inspiration
        count += len1
        
        # Total breath data
        len2 = len(Data_inp_exp[j].totalBreath)
        All_data[count:count+len2, :2] = np.tile([sg, 2], (len2, 1))
        All_data[count:count+len2, 2] = Data_inp_exp[j].totalBreath
        count += len2
    
    All_data = All_data[:count, :]
    savemat('AllData_varyingc1_totBreath1_phase2.mat', {'All_data': All_data})

if __name__ == "__main__":
    Varying_c1_phase2()
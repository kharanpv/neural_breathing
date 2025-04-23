import numpy as np
from scipy.io import savemat
import matplotlib.pyplot as plt
from import_handler import get_function_or_fallback 

# Import relevant functions from other files (with error handling)
parameters_phase2_paperC = get_function_or_fallback("parameters_phase2_paperC")
TrajectoryGenerator_3Nodes = get_function_or_fallback("TrajectoryGenerator_3Nodes")
findPattern = get_function_or_fallback("findPattern")

def Varying_c3_phase2():
    """Python implementation of Varying_c3_phase2.m"""
    try:
        # Load parameters (placeholder - need implementation)
        params1, params3, params4 = parameters_phase2_paperC()
        
        TotalTime = 4000
        memoryLen = params3[0]  # params3(1) in MATLAB
        activeThreshold = params3[1]  # params3(2)
        m = params3[3]  # params3(4)
        
        # Period calculation
        startPeriod = m + 1
        endPeriod = memoryLen - 1
        step_period = 5
        num_period = (endPeriod - startPeriod) // step_period

        # Data structure
        class BreathData:
            __slots__ = ['signal_period', 'expiration', 'inspiration', 'totalBreath']
            def __init__(self):
                self.signal_period = 0
                self.expiration = np.array([])
                self.inspiration = np.array([])
                self.totalBreath = np.array([])
        
        Data_inp_exp = []
        numData = 0

        for k in range(2, num_period + 1):
            signal_period = startPeriod + step_period * (k - 1)
            params3[2] = signal_period  # params3(3) in MATLAB
            totT = TotalTime + 2 * signal_period

            for _ in range(10):
                Net1, Net3, Net4 = TrajectoryGenerator_3Nodes(totT, params1, params3, params4)
                node1 = Net1[:, 0]

                # Optional plotting (first iteration only)
                if k == 2:
                    plt.figure(figsize=(12, 8))
                    plt.subplot(3, 1, 1)
                    plt.plot(node1, '*')
                    plt.title(f'Signal Period: {signal_period}')
                    plt.show()

                # Pattern detection
                starts = findPattern(node1, np.array([0, 1]))
                ends = findPattern(node1, np.array([1, 0]))
                
                if len(starts) > 3:
                    starts, ends = starts[1:], ends[1:]
                    minLen = min(len(starts), len(ends))
                    
                    if starts[0] < ends[0]:
                        number_1s = ends[:minLen] - starts[:minLen]
                        number_0s = starts[1:minLen] - ends[:minLen-1]
                    else:
                        number_1s = ends[1:minLen] - starts[:minLen-1]
                        number_0s = starts[:minLen] - ends[:minLen]

                    data = BreathData()
                    data.expiration = number_0s
                    data.inspiration = number_1s
                    data.totalBreath = starts[1:len(starts)-1] - starts[:len(starts)-2]
                    data.signal_period = signal_period
                    Data_inp_exp.append(data)
                    numData += 1

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
        savemat('VaryingC3_Phase_2.mat', {'All_data': All_data})
        return All_data

    except Exception as e:
        print(f"Error in Varying_c3_phase2: {str(e)}")
        return None

if __name__ == "__main__":
    data = Varying_c3_phase2()
    if data is not None:
        print(f"Successfully generated data with shape: {data.shape}")
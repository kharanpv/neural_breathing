import numpy as np
import matplotlib.pyplot as plt
from scipy.io import savemat
from import_handler import get_function_or_fallback 

# Import relevant functions from other files (with error handling)
parameters_phase3_paperC = get_function_or_fallback("parameters_phase3_paperC")
signalGenerator = get_function_or_fallback("signalGenerator")
f1 = get_function_or_fallback("f1")
f3_A = get_function_or_fallback("f3_A")
f4 = get_function_or_fallback("f4")

def TrajectoryGenerator_3Nodes_plot():
    """Python implementation of TrajectoryGenerator_3Nodes_plot.m"""
    try:
        # Load parameters (phase3 configuration)
        params1, params3, params4 = parameters_phase3_paperC()
        TotalTime = 2000

        # Generate control signals
        signal_period1 = params1[4]  # params1(5)
        c1 = signalGenerator(TotalTime, signal_period1)
        
        signal_period3 = params3[2]  # params3(3)
        c3 = signalGenerator(TotalTime, signal_period3)
        
        signal_period4 = params4[2]  # params4(3)
        c4 = signalGenerator(TotalTime, signal_period4)

        # Initialize networks
        memoryLen1 = params1[1]  # params1(2)
        n_pos1 = params1[2]      # params1(3)
        Net1 = np.zeros((TotalTime, memoryLen1 + n_pos1))
        
        memoryLen3 = params3[0]  # params3(1)
        Net3 = np.zeros((TotalTime, memoryLen3 + 1))
        
        memoryLen4 = params4[0]  # params4(1)
        Net4 = np.zeros((TotalTime, memoryLen4 + 1))

        # Initialize states
        current_state_Net1 = Net1[0, :].copy()
        current_state_Net3 = Net3[0, :].copy()
        current_state_Net4 = Net4[0, :].copy()
        x1 = current_state_Net1[0]
        x3 = current_state_Net3[0]
        x4 = current_state_Net4[0]

        # Generate trajectories
        for k in range(TotalTime):
            # Update network states
            next_state_Net1 = f1(current_state_Net1, x3, x4, c1[k], params1)
            next_state_Net3 = f3_A(current_state_Net3, c3[k], params3)
            next_state_Net4 = f4(current_state_Net4, x3, c4[k], params4)
            
            # Store states
            Net1[k, :] = next_state_Net1
            Net3[k, :] = next_state_Net3
            Net4[k, :] = next_state_Net4
            
            # Update current states
            current_state_Net1 = next_state_Net1.copy()
            current_state_Net3 = next_state_Net3.copy()
            current_state_Net4 = next_state_Net4.copy()
            x1 = current_state_Net1[0]
            x3 = current_state_Net3[0]
            x4 = current_state_Net4[0]

        # Prepare data for plotting
        eps = 0.00
        node1 = Net1[:, 0] + eps
        node3 = Net3[:, 0] + eps
        node4 = Net4[:, 0] + eps

        # Create figure
        plt.figure(figsize=(12, 8))
        
        # Plot X4
        plt.subplot(3, 1, 1)
        plt.plot(node4, '.b')
        plt.ylabel('X_4', fontsize=20)
        plt.gca().tick_params(labelsize=12)
        
        # Plot X3
        plt.subplot(3, 1, 2)
        plt.plot(node3, '.b')
        plt.ylabel('X_3', fontsize=20)
        plt.gca().tick_params(labelsize=12)
        
        # Plot X1
        plt.subplot(3, 1, 3)
        plt.plot(node1, '.b')
        plt.ylabel('X_1', fontsize=20)
        plt.xlabel('Step', fontsize=20)
        plt.gca().tick_params(labelsize=12)
        
        plt.tight_layout()
        plt.show()

        return Net1, Net3, Net4

    except Exception as e:
        print(f"Error in TrajectoryGenerator_3Nodes_plot: {str(e)}")
        return None, None, None

if __name__ == "__main__":
    Net1, Net3, Net4 = TrajectoryGenerator_3Nodes_plot()
    if Net1 is not None:
        print("Trajectories generated successfully")
        print(f"Net1 shape: {Net1.shape}, Net3 shape: {Net3.shape}, Net4 shape: {Net4.shape}")
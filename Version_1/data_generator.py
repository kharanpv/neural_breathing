import numpy as np
from scipy.io import savemat
from import_handler import get_function_or_fallback 

# Import relevant functions from other files (with error handling)
Varying_c1_phase3 = get_function_or_fallback("Varying_c1_phase3")
Varying_c1_phase2 = get_function_or_fallback("Varying_c1_phase2")
Varying_c3_phase3 = get_function_or_fallback("Varying_c3_phase3")
Varying_c3_phase2 = get_function_or_fallback("Varying_c3_phase2")
Varying_c4_phase3 = get_function_or_fallback("Varying_c4_phase3")

def dataGenerator_for_BoxPlot():
    """Python version of dataGenerator_for_BoxPlot.m"""
    # User choices (modify as needed)
    variable = 'c1'  # Options: 'c1', 'c3', 'c4'
    phase = 'phase3'  # Options: 'phase2', 'phase3'
    choice = f"{variable}_{phase}"

    # Dispatch to the appropriate function
    actions = {
        'c1_phase3': Varying_c1_phase3,
        'c1_phase2': Varying_c1_phase2,
        'c3_phase3': Varying_c3_phase3,
        'c3_phase2': Varying_c3_phase2,
        'c4_phase3': Varying_c4_phase3,
    }

    # Execute the chosen action
    if choice in actions:
        try:
            output_data = actions[choice]()  # Call the function
            print(f"Data generated for {choice}")
            savemat(f"AllData_{choice}_totBreath1.mat", {'All_data': output_data})
        except NotImplementedError as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")
    else:
        print("Warning: Invalid choice")

if __name__ == "__main__":
    dataGenerator_for_BoxPlot()
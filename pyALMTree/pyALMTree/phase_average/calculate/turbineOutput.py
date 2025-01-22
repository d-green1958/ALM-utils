def turbineOutput(
    case_path: str,
    calculate_rotor_performance: bool = True,
    calculate_blade_loads: bool = True,
):
    import os
    
    turbineOutput_path = os.path.join(case_path, "phaseAveraged-turbineOutput")
    results_path = os.path.join(turbineOutput_path, "result")
    if not os.path.exists(results_path):
        os.mkdir(results_path)
    
    for file in os.listdir(turbineOutput_path):
        if calculate_blade_loads:
            print(f"  --phase averaging {file}")
            raise NotImplementedError("Not implemented yet!")
            
        if calculate_rotor_performance:
            if file in ["thrust", "powerRotor", "torqueRotor"]:
                print(f"  --phase averaging {file}")
                file_path = os.path.join(turbineOutput_path, file)
                _calculate_performance(file_path, results_path)
                
                
                
                
def _calculate_performance(file_path, results_path):
    import os, pandas as pd, numpy as np
    
    df = pd.read_csv(file_path)
    grouped = df.groupby('bin')
    
    bin_values = np.array([])
    output_values = np.array([])
    
    for bin_value, group in grouped:
        # assuming index 4 is alway the value of interest
        key = group.keys()[4]
        
        # add values to arrays
        bin_values = np.append(bin_values, bin_value)
        output_values = np.append(output_values, np.mean(group[key]))
        
    output_df = pd.DataFrame()
    output_df["bin"] = bin_values
    output_df[os.path.basename(file_path)] = output_values
    
    destination = os.path.join(results_path, os.path.basename(file_path))
    output_df.to_csv(destination, index=False)  


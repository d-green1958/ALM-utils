import pandas as pd
import numpy as np

def turbineOutput_file(file_path, blade_data_file=False):
    with open(file_path, 'r') as f:
        header_line = f.readline().strip()
        # Split the header by four spaces
        headers = header_line.split('    ')
        
    # Read the rest of the file as a DataFrame
    data = pd.read_csv(file_path, delimiter=r'\s+', skiprows=1, header=None)
    
    number_of_headers = len(headers)
    number_of_columns = len(data.iloc[0,:])
    
    # if the final column contains blade data then combine it into an array
    if blade_data_file:
        blade_data_key = headers[-1]
        
        blade_data_columns = data.iloc[:, number_of_headers-1:]
        blade_data_arr = blade_data_columns.to_numpy()
                
        data = data.iloc[:,:number_of_headers-1]
        headers.remove(blade_data_key)
        data.columns = headers
        
        data[blade_data_key] = [row for row in blade_data_arr]
    else:
        if number_of_headers != number_of_columns:
            raise AttributeError("I think you forgot to use blade_data_file=True")
        data.columns = headers
    
    return data

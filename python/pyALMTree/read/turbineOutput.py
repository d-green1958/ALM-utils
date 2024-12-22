import pandas as pd
def turbineOutput_file(file_path):
    with open(file_path, 'r') as f:
        header_line = f.readline().strip()
        # Split the header by four spaces
        headers = header_line.split('    ')
        
    # Read the rest of the file as a DataFrame
    data = pd.read_csv(file_path, delimiter=r'\s+', skiprows=1, header=None)

    # Assign the headers to the DataFrame
    data.columns = headers
    return data

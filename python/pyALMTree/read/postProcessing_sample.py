import pandas as pd
import numpy as np

def postProcessing_sample_file(file_path: str) -> pd.DataFrame:
    """
    Read in a sample file from the postProcessing directory and return it as a pandas DataFrame. 
    
    Args:
        file_path (str): Path to file.

    Returns:
        pd.DataFrame: Dataframe containing file contents.
    """
    df = pd.read_csv(file_path)
    return df
    
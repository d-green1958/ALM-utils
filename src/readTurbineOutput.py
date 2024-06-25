import os
import numpy as np
import sys


def read_file(case_path, file_names):
    print(f"reading from {case_path}")
    
    # make sure turbineOutput exists
    turbine_output_path = os.path.join(case_path, "turbineOutput")
    if not os.path.isdir(turbine_output_path):
        print("no turbineOutput directory")
        sys.exit(1)
    
    # look for different runs
    run_dirs = os.listdir(turbine_output_path)
    if len(run_dirs) == 1:
        print(f"reading from results file {run_dirs[0]}")
        turbine_output_path = os.path.join(turbine_output_path, run_dirs[0])
    elif len(run_dirs) > 1:
        # if there are multiple ask for one
        print(f"multiple results paths found:")
        for run_dir in run_dirs:
            print(f"-- {run_dir} --")

        choice_made = False
        while not choice_made:
            choice = input("please choose one")
            if choice not in run_dirs:
                print("invalid response")
            else:
                choice_made = True
                turbine_output_path = os.path.join(turbine_output_path, choice)
         
    # create dictionary for data storage       
    data = {}
    for file_name in file_names:
        # check file exists
        file_path = os.path.join(turbine_output_path, file_name)
        if not os.path.exists(file_path):
            print(f"no file: {file_path}")
        
        print(f"-- reading {file_name} --", end=' ')
        
        # read in data from file
        data[file_name] = np.genfromtxt(file_path, delimiter=' ')
        print(" |done|")
        
    # return the dict
    return data
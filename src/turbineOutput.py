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



def process_spanwise_forces(data, keys = ["axialForce", "tangentialForce"]):
    # here the keys argument has been included since might also want to plot normal or chordwise forces
    # but this has not been implemented into the main calling this.
    
    forces = {}
    times_defined = False
    for key in keys:
        if key not in data.keys():
            print(f"{key} not in data")
            sys.exit(1)
            
        force_data = data[key]
        if len(np.unique(force_data[:,0])) != 1:
            print("number of rotors != 1 [not implemented]")
            sys.exit(1)
        if len(np.unique(force_data[:,1])) != 3:
            print("number of blades != 3 [not implemented]")
            sys.exit(1)
        
        blade_forces = [] # [blade number][time step][position on blade]
        if times_defined == True:
            if times.any() != np.unique(force_data[:,2]).any():
                print("inconsistent times between force keys")
                sys.exit(1)
        
        times = np.unique(force_data[:,2])
        times_defined = True
        blade_ids = np.unique(force_data[:,1])
        
        for blade_id in blade_ids:
            inds = (force_data[:,1] == blade_id)
            temp = force_data[inds,4::]
            blade_forces.append(temp)
        
        forces[key] = blade_forces
        forces["times"] = times
                    
    return times, forces

def process_radius(data):
    keys = data.keys()
    if "radiusC" not in keys:
        print("radiusC not found in data")
        sys.exit(1)
    
    rad_data = data["radiusC"]
    
    # get number of rotors
    rotor_ids = np.unique(rad_data[:,0])
    if len(rotor_ids) != 1:
        print("number of rotors != 1")
        sys.exit(1)
    
    # get number of blades
    blade_ids = np.unique(rad_data[:,1])
    if len(blade_ids) != 3:
        print("number of blades != 3 [not implemented, may cause issues]")
        sys.exit(1)
    
    # check for symmetry of rotor
    radial_pos = rad_data[:,2::]
    if (radial_pos[0].any() != radial_pos[1].any()) or (radial_pos[1].any() != radial_pos[2].any()):
        print("rotor is assymetric [not implemented]")
        sys.exit(1)
    
    return radial_pos[0]

def process_power_and_thrust(data):
    keys = ["powerRotor", "thrust"]
    output = {}
    
    times_set = False
    for key in keys:
        if key not in data.keys():
            print(f"{key} not in data")
            sys.exit(1)
        
        key_data = data[key]
        if times_set:
            if key_data[:,1].any() != times.any():
                print("there are differences in the time series between rotor and power")
                sys.exit(1)
        
        times = key_data[:,1]
        times_set = True
        
        output[key] = key_data[:,3]
    output["times"] = times
    
    return times, output
            
        
        
        
        
        
         
                      
    
    
    
    
    return None, None, None
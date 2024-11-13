
import ALM_utils

def process_samples(postProcessing_path, sample_dirs):
    print("--samples")
    import numpy as np
    sample_dirs_stripped = np.unique([dir.replace("Inst","").replace("Stat","") for dir in sample_dirs])
    
    for sample in sample_dirs_stripped:
        if (f"{sample}Inst" in sample_dirs) & (f"{sample}Stat" in sample_dirs):
            print(f"  --{sample}")  
            inst_path = os.path.join(postProcessing_path, f"{sample}Inst")
            stat_path = os.path.join(postProcessing_path, f"{sample}Stat")
            
            print(os.listdir(inst_path))
            ALM_utils.sample.plot.general()

    


def process_probes(postProcessing_path, probe_dirs):
    return




if __name__ == "__main__":
    import os
    
    cwd = os.getcwd()
    postProcessing_path = os.path.join(cwd, "postProcessing")
    turbineOutput_path = os.path.join(cwd, "turbineOutput")
    
    turbineOutput_exists = os.path.exists(turbineOutput_path)
    postProcessing_exists = os.path.exists(postProcessing_path)
    
    print(f"case name: {cwd}")
    if postProcessing_exists:
        print("\nfound postProcessing dir")
        
        sample_dirs = []
        probe_dirs = []
        
        
        list_of_postProcessing_dirs = os.listdir(postProcessing_path)
        for dir in list_of_postProcessing_dirs:
            if "sample" in dir.lower():
                sample_dirs.append(dir)
            elif "probe" in dir.lower():
                probe_dirs.append(dir)
            
        if len(sample_dirs) != 0:
            process_samples(postProcessing_path, sample_dirs)
        if len(probe_dirs) != 0:
            process_probes(postProcessing_path, probe_dirs)

    else:
        print("ERR: could not find postProcessing dir")
        
    if turbineOutput_exists:
        print("\nfound turbineOutput dir")
    else:
        print("ERR: could not find turbineOutput dir")
    
    

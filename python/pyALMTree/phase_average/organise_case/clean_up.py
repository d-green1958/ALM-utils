def clean_up(case_path: str):
    import os
    import shutil
    for folder in os.listdir(case_path):
        if "phaseAveraged" in folder:
            folder_path = os.path.join(case_path, folder)
            
            for subfolder in os.listdir(folder_path):
                subfolder_path = os.path.join(folder_path, subfolder)
                
                if os.path.isfile(subfolder_path):
                    print(f"  --cleaning {subfolder}")
                    if "result" in subfolder:
                        continue
                    else:
                        os.remove(subfolder_path)
                        continue
                
                print(f"  --cleaning {subfolder}")
                for subsubfolder in os.listdir(subfolder_path):
                    
                    subsubfolder_path = os.path.join(subfolder_path, subsubfolder)
                    if "result" in subsubfolder:
                        continue

                    if os.path.isfile(subsubfolder_path):
                        os.remove(subsubfolder_path) 
                    elif os.path.isdir(subsubfolder_path):
                        shutil.rmtree(subsubfolder_path)  

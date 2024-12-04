def turbineOutput(
    case_path: str,
    bin_size: float,
    time_start: float = 0,
    turbineOutput_subdir: str = None,
    organise_rotor_performance: bool = True,
    organise_blade_loads: bool = True,
):
    """_summary_

    Args:
        case_path (str): path to case
        bin_size (float): size of bins in degrees
        time_start (float): time to start organising after. Defaults to 0.
        turbineOutput_subdir (str, optional): turbineOutput subdirectory to read from. Defaults to None in which if only one directory exists this will be used..
        organise_rotor_performance (bool, optional): organise the rotor performances. Defaults to True.
        organise_blade_loads (bool, optional): organise the blade loads. Defaults to True.
    """
    import os
    import pandas as pd
    import numpy as np

    turbineOutput_path = os.path.join(case_path, "turbineOutput")
    if not os.path.exists(turbineOutput_path):
        raise FileExistsError("Cannot Find turbineOutput")

    subdirs = os.listdir(turbineOutput_path)
    if len(subdirs) > 1:
        if turbineOutput_subdir == None:
            raise ValueError("No turbineOutput subdirectory provided")

        turbineOutput_subdir_path = os.path.join(
            turbineOutput_path, turbineOutput_subdir
        )
        if not os.path.exists(turbineOutput_subdir_path):
            raise FileExistsError(
                "turbineOutput path subdirectory provided does not exist"
            )
    else:
        turbineOutput_subdir_path = os.path.join(turbineOutput_path, subdirs[0])

    rotationAngle_path = os.path.join(turbineOutput_subdir_path, "rotationAngle")
    if not os.path.exists(rotationAngle_path):
        FileExistsError("turbineOutput/subdir/rotationAngle does not exist")

    df_rotation_angle = pd.read_csv(rotationAngle_path, sep=r"\s+")

    # for now assume a single turbine
    if np.unique(df_rotation_angle["#Turbine"]) != [0]:
        raise NotImplementedError("More than one turbine - not implemented")

    # determine the rotation direction
    if np.max(df_rotation_angle["rotAngle(deg)"]) > 0:
        bins = np.arange(0, 360 + bin_size / 2, bin_size)
    else:
        bins = np.arange(-360, bin_size / 2, bin_size)

    times = df_rotation_angle["Time(s)"]
    times_float = np.array(times, dtype=float)
    bin_inds = np.digitize(df_rotation_angle["rotAngle(deg)"], bins)

    # create new dir to place phase avereaged values in
    os.makedirs(os.path.join(case_path, "phaseAveraged-turbineOutput"), exist_ok=True)
    phaseAveraged_postProcessing_path = os.path.join(
        case_path, "phaseAveraged-turbineOutput"
    )

    for file in os.listdir(turbineOutput_subdir_path):
        file_path = os.path.join(turbineOutput_subdir_path, file)

        if organise_rotor_performance:
            if file in ["thrust", "powerRotor", "torqueRotor"]:
                print(f"  --organising {file}")
                _prep_file(
                    phaseAveraged_postProcessing_path,
                    file_path,
                    bins,
                    bin_inds,
                    times_float,
                    time_start,
                )
                None

        if organise_blade_loads:
            if file in ["tangentialForce", "normalForce", "axialForce"]:
                None
                # _prep_file(
                #     phaseAveraged_postProcessing_path,
                #     file_path,
                #     bins,
                #     bin_inds,
                #     times_float,
                #     multiple_blades=True,
                # )


def _prep_file(
    phaseAveraged_turbineOutput_path,
    file_path,
    bins,
    bin_inds,
    times_float,
    time_start,
    multiple_blades=False,
):
    import pandas as pd, os, numpy as np

    df = pd.read_csv(file_path, sep=r"\s+")

    if "Time(s)" not in df.keys():
        raise KeyError(f"Time(s) not a key in {file_path}")

    bin_names = np.array("outside")
    for i in range(1, len(bins)):
        bin_names = np.append(bin_names, f"{bins[i-1]}_{bins[i]}")

    if not multiple_blades:
        df["bin"] = bin_names[bin_inds]
        destination = os.path.join(
            phaseAveraged_turbineOutput_path, os.path.basename(file_path)
        )
        
        df = df[df["Time(s)"] > time_start]
        
        df.to_csv(destination)
    else:
        # phases = np.array([])
        # for time in df["Time(s)"]:
        #     # print(time)
        #     ind = np.argmin(np.abs(float(time) == times_float))
        #     # print(ind)

        # difficult to read in file due to terrible naming system!!!

        raise NotImplementedError("Not implemented")

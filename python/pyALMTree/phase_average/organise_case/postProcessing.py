def postProcessing(
    case_path: str,
    bin_size: float,
    turbineOutput_subdir: str = None,
    organise_samples: bool = True,
    organise_surfaces: bool = True,
):
    """organise the post processing path into phase averaged bins using the rotorAngle file.

    Args:
        case_path (str): path to case
        bin_size (float): bin size in degrees
        turbineOutput_subdir (str, optional): Name of turbineOutput subdir. Defaults to None in which case if only one subdir exists it will assume that.
        organise_samples (bool, optional): Organise the sample files. Defaults to True.
        organise_surfaces (bool, optional): Organise the surface files. Defaults to True.
    """
    import os
    import pandas as pd
    import numpy as np

    postProcess_path = os.path.join(case_path, "postProcessing")
    if not os.path.exists(postProcess_path):
        raise FileExistsError("Cannot Find postProcessing")

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
    os.makedirs(os.path.join(case_path, "phaseAveraged-postProcessing"), exist_ok=True)
    phaseAveraged_postProcessing_path = os.path.join(
        case_path, "phaseAveraged-postProcessing"
    )

    for dir in os.listdir(postProcess_path):
        if organise_surfaces:
            if "surface" in dir:
                surface_dir_path = os.path.join(postProcess_path, dir)
                _organise_surfaces(
                    phaseAveraged_postProcessing_path,
                    surface_dir_path,
                    bins,
                    bin_inds,
                    times_float,
                )
        if organise_samples:
            if "sample" in dir:
                sample_dir_path = os.path.join(postProcess_path, dir)
                _organise_samples(
                    phaseAveraged_postProcessing_path,
                    sample_dir_path,
                    bins,
                    bin_inds,
                    times_float,
                )


def _organise_samples(
    phaseAveraged_postProcessing_path, sample_dir_path, bins, bin_inds, times_float
):
    import os
    import numpy as np
    import shutil

    phaseAveraged_sample_path = os.path.join(
        phaseAveraged_postProcessing_path, os.path.basename(sample_dir_path)
    )
    os.makedirs(phaseAveraged_sample_path, exist_ok=True)

    bin_names = np.array("outside")
    for i in range(1, len(bins)):
        bin_names = np.append(bin_names, f"{bins[i-1]}-{bins[i]}")

    for name in bin_names:
        os.makedirs(os.path.join(phaseAveraged_sample_path, name), exist_ok=True)

    for time_dir in os.listdir(sample_dir_path):
        time_dir_path = os.path.join(sample_dir_path, time_dir)
        time_dir_str = time_dir
        time_dir_float = float(time_dir)
        if time_dir_float in times_float:
            ind = np.where(time_dir_float == times_float)[0][0]
            bin_ind = bin_inds[ind]

            # copy the files to the bin
            bin_path = os.path.join(phaseAveraged_sample_path, bin_names[bin_ind])
            for file in os.listdir(time_dir_path):
                phase_averaged_file_folder_path = os.path.join(bin_path, file)

                if not os.path.exists(phase_averaged_file_folder_path):
                    os.makedirs(phase_averaged_file_folder_path)

                location = os.path.join(time_dir_path, file)
                destination = os.path.join(
                    phase_averaged_file_folder_path, time_dir_str
                )

                shutil.copy(location, destination)

        else:
            raise LookupError(
                f"Could not find sample time {time_dir} in rotationAngle times"
            )


def _organise_surfaces(
    phaseAveraged_postProcessing_path, surface_dir_path, bins, bin_inds, times_float
):
    import os
    import numpy as np
    import shutil

    phaseAveraged_surface_path = os.path.join(
        phaseAveraged_postProcessing_path, os.path.basename(surface_dir_path)
    )
    os.makedirs(phaseAveraged_surface_path, exist_ok=True)

    bin_names = np.array("outside")
    for i in range(1, len(bins)):
        bin_names = np.append(bin_names, f"{bins[i-1]}-{bins[i]}")

    for name in bin_names:
        os.makedirs(os.path.join(phaseAveraged_surface_path, name), exist_ok=True)

    for time_dir in os.listdir(surface_dir_path):
        time_dir_path = os.path.join(surface_dir_path, time_dir)
        time_dir_str = time_dir
        time_dir_float = float(time_dir)
        if time_dir_float in times_float:
            ind = np.where(time_dir_float == times_float)[0][0]
            bin_ind = bin_inds[ind]

            # copy the files to the bin
            bin_path = os.path.join(phaseAveraged_surface_path, bin_names[bin_ind])
            for file in os.listdir(time_dir_path):
                phase_averaged_file_folder_path = os.path.join(bin_path, file)

                if not os.path.exists(phase_averaged_file_folder_path):
                    os.makedirs(phase_averaged_file_folder_path)

                location = os.path.join(time_dir_path, file)
                destination = os.path.join(
                    phase_averaged_file_folder_path, time_dir_str
                )

                shutil.copy(location, destination)

        else:
            raise LookupError(
                f"Could not find sample time {time_dir} in rotationAngle times"
            )

def postProcessing(
    case_path: str,
    calculate_samples: bool = True,
    calculate_surfaces: bool = True,
):
    """take the organised phaseAverage directory and calcualte the phase averaged results which is then stored in the results directory

    Args:
        case_path (str): Path to case.
        calculate_samples (bool, optional): Flag for calcualting the phase avereaged samples. Defaults to True.
        calculate_surfaces (bool, optional): flag for calcualting the pahse averaged surfaces. Defaults to True.
    """
    import os

    postProcessing_path = os.path.join(case_path, "phaseAveraged-postProcessing")

    for folder in os.listdir(postProcessing_path):
        if calculate_samples:
            if "sample" in folder:
                print(f"  --phase averaging {folder}")
                _calcualte_sample(os.path.join(postProcessing_path, folder))

        if calculate_surfaces:
            if "surface" in folder:
                print(f"  --phase averaging {folder}")
                _calculate_surface(os.path.join(postProcessing_path, folder))


def _calcualte_sample(sample_folder_path: str):
    import os, pandas as pd

    bins = os.listdir(sample_folder_path)
    results_path = os.path.join(sample_folder_path, "result")
    os.makedirs(results_path, exist_ok=True)

    # for each bin
    for bin in bins:
        bin_path = os.path.join(sample_folder_path, bin)

        # for each sample type
        for sample_type_folder in os.listdir(bin_path):
            sample_type_folder_path = os.path.join(bin_path, sample_type_folder)

            destination_folder_path = os.path.join(results_path, sample_type_folder)
            if not os.path.exists(destination_folder_path):
                os.mkdir(destination_folder_path)

            # for each time
            dfs = []
            for time_file in os.listdir(sample_type_folder_path):
                file_path = os.path.join(sample_type_folder_path, time_file)
                dfs.append(pd.read_csv(file_path))

            mean_df = sum(dfs) / len(dfs)

            # now save
            mean_df.to_csv(
                os.path.join(os.path.join(destination_folder_path, bin + ".csv")),
                index=False,
            )

def _calculate_surface(surface_folder_path: str):
    raise NotImplementedError("Not implemented yet")
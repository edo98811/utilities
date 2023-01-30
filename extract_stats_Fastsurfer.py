import zipfile
import os
import pandas as pd
import shutil
import csv
import re


def extract_path(filename, base_path):
    # all_path = []

    subjs_path = []
    for path, subdirs, files in os.walk(base_path):
        if path.split("/")[-1] == 'stats':
            for name in files:
                if name == filename:
                    subjs_path.append(path + "/" + name)

    if not subjs_path:
        return False

    return subjs_path


def stats(subj_paths):
    df_dict = {}

    first = True
    for n, path in enumerate(subj_paths):
        print("extracting stats for subject " + str(n + 1) + ", path:" + path)
        with open(path, "r") as file:
            data = file.readlines()

        for i, line in enumerate(data):

            # parte 1
            match = re.match(r"^# Measure (\w+).+(\d | \d+\.\d+),\s\w+$", line)

            if match:
                if first:
                    df_dict[match.group(1)] = [match.group(2)]
                    print(df_dict)
                else:
                    df_dict[match.group(1)].append(
                        match.group(2))

            # parte 2
            if not line.startswith("#"):
                values = line.strip().split()
                print(values)
                if first:
                    df_dict[values[4] + " volume"] = [values[3]]
                else:
                    df_dict[f"{values[4]} volume"].append(values[3])

        first = False

    return pd.DataFrame.from_dict(df_dict, orient='columns')


if __name__ == "__main__":
    base_path = '/media/neuropsycad/disk12t/EdoardoFilippiMasterThesis/FastSurfer_Output_Comparison_AD/'

    # the filename of the stats to extract
    filename = 'aseg.stats'

    subj_paths = extract_path(filename, base_path)
    if subj_paths:
        print("stats file found for " + str(len(subj_paths)) + " subjects")
        stats(subj_paths).to_csv("aseg.csv")
    else:
        print("no file found")

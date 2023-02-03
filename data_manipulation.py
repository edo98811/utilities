

import nibabel.freesurfer as fs
import nibabel as nib
import os
import json
import re

def read_label(label_name, path=""):
    return fs.read_annot(str(path + label_name))

def read_img(img_name, path = ""):
    return nib.load(str(path + img_name))

def list_files_all(dir,imgname):
    """
    input
        imgname = str
        filetype = str, default = nii.gz
    """

    r_img = []

    # fl_len = len(filetype.split("."))
    # print(fl_len)
    # print(dir)
    # print(filetype)
    # print(filetype.split("."))
    for root, dirs, files in os.walk(dir):
        #r_all.append(os.path.join(root))
        #print(files)
        for name in files:
            if name == imgname:# and l_name[-fl_len:-1] == filetype:
                r_img.append(os.path.join(root, name))

    return r_img
def list_files(dir,filename):
    """
    input
        imgname = str
    """
    r_img = []

    for root, dirs, files in os.walk(dir):
        for name in files:
            if name == filename:
                r_img.append(os.path.join(root, name))

    return r_img
def write_dict(all_files, filename):
    json_object = json.dumps(all_files, indent=4)

    with open(filename, "w") as outfile:
        outfile.write(json_object)

def write_txt(list, filename):
    with open(filename, 'w') as f:
        for item in list:
            f.write(item + '\n')

def load_txt(filename):
    with open(filename, "r") as file:
        data = file.read()
        return data.split("\n")

def load_dict(filename):
    with open(filename, "r") as infile:
        img_dict = json.load(infile)
    return img_dict

def convert_img(img_list):
    if not os.path.isdir("../dataset"):
        os.makedirs("../dataset")

    for img_name in img_list:

        img = nib.load(img_name)

        subj = img_name.split("/")[-3]
        nib.save(img, f"../dataset/{subj}_T1.nii.gz")



def select_paths_and_save(subject_to_select, destination_file, all_paths_file):

    subj_numbers = load_txt(subject_to_select)
    subj_paths = []

    subj_paths_all = load_txt(all_paths_file)

    for subj_number in subj_numbers:
        for subj_path in subj_paths_all:
           # print(subj_number)
           # print(len(subj_path.split("/")))
            if len(subj_path.split("/")) > 3:
                match = re.split("sub-", subj_path.split("/")[-4])
                # print(match)
                if subj_number == match[1]:
                    subj_paths.append(subj_path)

    write_txt(subj_paths, destination_file)
    return subj_paths
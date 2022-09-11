import subprocess
import os
import logging
from tkinter import filedialog

"""
this file is largely independent of all other files in the `source` directory
it seeks to create a log of all of the environments and specifications
so that this package is reproducible to other users
"""

# set up the logging level
logging.basicConfig(level=logging.INFO)

# find the directory the reproducibility file is in
def get_file_dir():
    """
    retrieves the directory the reproducibility file is in

    @returns file_dir = directory to write files
    """
    full_path = os.path.abspath(__file__)
    file_dir = full_path.split("/reproducibility.py")[0]
    logging.info(f"WRITING FILES TO:\n\t{file_dir}")
    return file_dir


# 1) save an explicit specification list
def save_exp_spec_list(file_dir: str):
    """
    saves the explicit specification list of packages for the conda environment

    @param file_dir = directory to save the file in
    @returns output = output of the OS system call
    """
    spec_list_fn = os.path.join(file_dir, "CONDA_SPEC_LIST.txt")
    command = f"conda list --explicit > {spec_list_fn}"
    logging.info(f"SAVING EXPLICIT SPECIFICATION FILE VIA:\n\t{command}")
    output = subprocess.check_output(args=command, shell=True)
    return output


# 2) create an environment YAML file
def save_env_yml(file_dir: str):
    """
    saves the conda environment YAML file

    @param file_dir = directory to save the file in
    @returns output = output of the OS system call
    """
    env_yml_fn = os.path.join(file_dir, "CONDA_ENVIRONMENT.yml")
    command = f"conda env export > {env_yml_fn}"
    logging.info(f"SAVING ENVIRONMENT YAML FILE VIA:\n\t{command}")
    output = subprocess.check_output(args=command, shell=True)
    return output


# 3) create a cross platform environment YAML file with only packages
#    we've explicitly asked for/downloaded
def save_xenv_yml(file_dir: str):
    """
    saves the cross platform version of the conda environment YAML file

    @param file_dir = directory to save the file in
    @returns output = output of the OS system call
    """
    xenv_yml_fn = os.path.join(file_dir, "CONDA_ENVIRONMENT_XPLATFORM.yml")
    command = f"conda env export --from-history > {xenv_yml_fn}"
    logging.info(f"SAVING CROSS PLATFORM ENVIRONMENT YAML FILE VIA:\n\t{command}")
    output = subprocess.check_output(args=command, shell=True)
    return output


# allow the file to be run on its own as well
if __name__ == "__main__":
    # retrieve directory to write in
    file_dir = get_file_dir()
    # write all reproducibility files
    save_exp_spec_list(file_dir=file_dir)
    save_env_yml(file_dir=file_dir)
    save_xenv_yml(file_dir=file_dir)

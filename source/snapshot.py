import os
import source.utils as utils
from typing import Dict
import source.constants as constants
import json
import tkinter


def prep_snapshot_env(
    dirname: str, prefix: str, labels: Dict[str, tkinter.Label]
) -> str:
    """
    constructs a filename from the given round number in labels and in the
    given directory creating it if it does not exist

    @param dirname = directory to create the snapshot
    @param prefix = prefix of the snapshot save files
    @param labels = labels of the given environment
    @returns filename = filename to write the snapshot to
    """
    # get the file directory
    full_path = os.path.abspath(__file__)
    file_dir = full_path.split("/snapshot.py")[0]
    # replace current directory with ideal
    dirname = file_dir.replace("source", dirname)
    # create the directory if not yet done
    _ = utils.create_dir_if_none(dirname=dirname)
    # retrieve the round number
    round_num = labels["rounds"]["text"].split(" ")[0]
    # append the prefix
    filename = f"{prefix}{round_num}.json"
    # join with the directory
    filename = os.path.join(dirname, filename)
    return filename


def take_snapshot(cell_objects: Dict, labels: Dict[str, tkinter.Label]):
    """
    takes a snapshot of all of the cells and saves it to the snapshot directory

    @param cell_objects = cells to save
    @param labels = labels of the given environment
    """
    # get the filename
    filename = prep_snapshot_env(
        dirname=constants.SNAPSHOT_DIRNAME,
        prefix=constants.SNAPSHOT_FILENAME_PREFIX,
        labels=labels,
    )
    # create tracking variable for all cells
    cell_snaps = {}
    # save all attributes for all of the cells by taking their snaps
    for cell_id, cell_object in cell_objects.items():
        cell_snap = cell_object.get_snap()
        cell_snaps[cell_id] = cell_snap
    # dump the data in JSON format into the given file
    with open(filename, "wt") as f:
        f.writelines(json.dumps(cell_snaps))

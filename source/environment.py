import source.utils as utils
import source.constants as constants
import source.cell as cell
from typing import Dict
# import packages
import tkinter

# create tkinter based canvas
def create_canvas():
    # instantiate application window
    window = tkinter.Tk()
    # name application window
    window.title(constants.WINDOW_NAME)
    # let it fill empty space (we have 1 row, 1 col)
    window.columnconfigure(0, weight=1)
    window.rowconfigure(0, weight=1)
    # create the canvas
    canvas = tkinter.Canvas(
        window,
        width=constants.WINDOW_WIDTH,
        height=constants.WINDOW_HEIGHT,
        background=constants.BKGD_COLOR
    )
    # start from middle centered to the upper left (in param sticky)
    canvas.grid(column=0, row=0, sticky=tkinter.NW)
    return window, canvas


# create ideal sequences
def create_ideal_seqs():
    """
    instantiates ideal sequences based on gene sizes defined in constants

    @returns ideal_seqs = idealized sequences that are randomly generated
    """
    ideal_seqs = {
        "digest": utils.gen_genome(size=constants.DIGEST_SIZE),
        "move": utils.gen_genome(size=constants.MOVE_SIZE),
        "mutate": utils.gen_genome(size=constants.MUTATE_SIZE)
    }
    return ideal_seqs


# create cells
def simulate_cells(
    n_cells: int,
    ideal_seqs: Dict[str, str]
):
    """
    creates cells and simulates their evolution and growth

    @param n_cells = number of cells to start with
    @param ideal_seqs = the idealized sequence to compare the cells with
    """
    # create the cells
    cells = []
    for _ in range(n_cells):
        cells.append(cell.Cell(traits=constants.CELL_TRAITS, ideal_seqs=ideal_seqs))
import source.utils as utils
import source.constants as constants
import source.cell as cell
from typing import Dict, Tuple
import time
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
        background=constants.BKGD_COLOR,
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
        "mutate": utils.gen_genome(size=constants.MUTATE_SIZE),
    }
    return ideal_seqs


# create cells
def create_cells(
    window: tkinter.Tk, canvas: tkinter.Canvas, n_cells: int, ideal_seqs: Dict[str, str]
) -> Tuple:
    """
    creates cells for the environment and simulation

    @param window = tkinter window to create a canvas in and update
    @param canvas = tkinter canvas to draw and manipulate objects in
    @param n_cells = number of cells to start with
    @param ideal_seqs = the idealized sequence to compare the cells with
    @returns cell_objects = map of cell memory id to their objects
    @returns cell_drawings = map of cell memory id to their canvas drawings
    """
    # create the cells
    cell_objects = {}
    cell_drawings = {}
    for _ in range(n_cells):
        # save the cells using their memory id
        cell_object = cell.Cell(traits=constants.CELL_TRAITS, ideal_seqs=ideal_seqs)
        cell_id = id(cell_object)
        cell_objects[cell_id] = cell_object
        # retrieve cell attributes
        position = cell_object.get_position()
        radius = cell_object.get_radius()
        color = cell_object.get_color()
        # draw the cells
        cell_drawing = utils.draw_circular_object(
            canvas=canvas,
            position=position,
            radius=radius,
            fill_color=color,
            outline_color=constants.CELL_OUTLINE_COLOR,
        )
        # save the cell drawing via its memory id
        cell_drawings[cell_id] = cell_drawing
    # update the canvas with the cells
    window.update()
    return (
        cell_objects,
        cell_drawings,
    )


def move_cells(
    window: tkinter.Tk,
    canvas: tkinter.Canvas,
    cell_objects: Dict[str, cell.Cell],
    cell_drawings: Dict,
):
    """
    moves all of the cells and shifts the cells by their movement

    @param window = tkinter window to update
    @param canvas = tkinter canvas where the objects are drawn
    @param cell_objects = map of cell memory id to their objects
    @param cell_drawings = map of cell memory id to their canvas drawings
    """
    # move each cell
    for cell_id, cell_object in cell_objects.items():
        # calculate the movement
        cell_object.move()
        # retrieve cell attributes
        position = cell_object.get_position()
        radius = cell_object.get_radius()
        cell_drawing = cell_drawings[cell_id]
        # update the drawing
        utils.update_circular_object(
            canvas=canvas,
            position=position,
            radius=radius,
            drawing=cell_drawing,
        )
    # update the window
    window.update()


def simulate_cells(
    window: tkinter.Tk, canvas: tkinter.Canvas, n_cells: int, ideal_seqs: Dict[str, str]
):
    """
    creates cells and simulates their evolution and growth

    @param window = tkinter window to create a canvas in and update
    @param canvas = tkinter canvas to draw and manipulate objects in
    @param n_cells = number of cells to start with
    @param ideal_seqs = the idealized sequence to compare the cells with
    """
    # create the cells
    cell_objects, cell_drawings = create_cells(
        window=window, canvas=canvas, n_cells=n_cells, ideal_seqs=ideal_seqs
    )
    # simulate their movement
    while True:
        # move the cells and update the objects
        move_cells(
            window=window,
            canvas=canvas,
            cell_objects=cell_objects,
            cell_drawings=cell_drawings,
        )
        # pause between rounds
        time.sleep(1)

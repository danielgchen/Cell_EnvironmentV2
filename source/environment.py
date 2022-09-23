import source.utils as utils
import source.constants as constants
import source.snapshot as snapshot
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
    window.rowconfigure(2, weight=1)
    # create the canvas
    canvas = tkinter.Canvas(
        window,
        width=constants.WINDOW_WIDTH,
        height=constants.WINDOW_HEIGHT,
        background=constants.BKGD_COLOR,
    )
    # start from upper left (in param sticky)
    canvas.grid(row=2, column=0, sticky=tkinter.NW)
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


def reap_cells(
    window: tkinter.Tk,
    canvas: tkinter.Canvas,
    cell_objects: Dict[str, cell.Cell],
    cell_drawings: Dict,
):
    """
    checks the health of all the cells and kills them if their energy is negative

    @param window = tkinter window to update
    @param canvas = tkinter canvas where the objects are drawn
    @param cell_objects = map of cell memory id to their objects
    @param cell_drawings = map of cell memory id to their canvas drawings
    """
    # instantiate new tracking objects
    new_cell_objects = {}
    new_cell_drawings = {}
    # check the health of each cell
    for cell_id, cell_object in cell_objects.items():
        # see if the cell is alive
        is_alive = cell_object.is_alive()
        # if the cell is alive add to new trackers
        if is_alive:
            new_cell_objects[cell_id] = cell_objects[cell_id]
            new_cell_drawings[cell_id] = cell_drawings[cell_id]
        # remove it from the canvas if the cell is dead
        else:
            canvas.delete(cell_drawings[cell_id])
    # reassign old trackers with new values
    cell_objects = new_cell_objects
    cell_drawings = new_cell_drawings
    # update the window
    window.update()


def create_labels(window: tkinter.Tk):
    """
    creates statistic labels to display under the exit button

    @param window = tkinter window to create a canvas in and update
    @returns labels = map of labels with key being the title of each one
    """
    # create tracker
    labels = {}
    # add the round label
    labels["rounds"] = tkinter.Label(window, text="0 rounds")
    labels["rounds"].grid(row=0, column=0, sticky=tkinter.NW)
    # add the n-cells label
    labels["cells"] = tkinter.Label(window, text="0 cells")
    labels["cells"].grid(row=1, column=0, sticky=tkinter.NW)
    return labels


def update_labels(labels: Dict[str, tkinter.Label], n_cells: int):
    """
    updates the labels with new round numbers and new n-cells

    @param labels = map of labels with key being the title of each one
    @param n_cells = new number of cells present in the environment
    """
    # get the current round number
    round_num = int(labels["rounds"]["text"].split(" ")[0])
    # update the round number
    labels["rounds"]["text"] = f"{round_num + 1} rounds"
    # update the number of cells
    labels["cells"]["text"] = f"{n_cells} cells"


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
    # create the labels
    labels = create_labels(window=window)
    # update the labels
    update_labels(labels=labels, n_cells=len(cell_objects))
    # take the initial snapshot
    snapshot.take_snapshot(cell_objects=cell_objects, labels=labels)
    # simulate their movement
    while True:
        # move the cells and update the objects
        move_cells(
            window=window,
            canvas=canvas,
            cell_objects=cell_objects,
            cell_drawings=cell_drawings,
        )
        # kill the cells if needed
        reap_cells(
            window=window,
            canvas=canvas,
            cell_objects=cell_objects,
            cell_drawings=cell_drawings,
        )
        # update the labels
        update_labels(labels=labels, n_cells=len(cell_objects))
        # take the general snapshot
        snapshot.take_snapshot(cell_objects=cell_objects, labels=labels)
        # pause between rounds
        time.sleep(constants.ROUND_SLEEP)

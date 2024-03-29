from multiprocessing.sharedctypes import Value
import numpy as np
import source.utils as utils
import source.constants as constants
import source.vent as vent
import source.snapshot as snapshot
import source.cell as cell
from typing import Dict, Tuple
import time
import tkinter
import logging

# create debugger
logging.basicConfig(filename="Log.log", level=logging.INFO)

# create tkinter based canvas
def create_canvas():
    """
    creates canvas for all elements to live in and utilizes constants
    to create this canvas and window using Tkinter

    @returns window = window canvas lives in
    @returns canvas = canvas to draw objects in
    """
    # debugging message
    logging.info("creating canvas")
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
    # debugging message
    logging.info("creating ideal sequences")
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
    # debugging message
    logging.info("creating cells")
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


# create vents
def create_vents(window: tkinter.Tk, canvas: tkinter.Canvas, n_vents: int) -> Tuple:
    """
    creates cells for the environment and simulation

    @param window = tkinter window to create a canvas in and update
    @param canvas = tkinter canvas to draw and manipulate objects in
    @param n_vents = number of vents to start with
    @returns vent_objects = map of vent memory id to their objects
    @returns vent_drawings = map of vent memory id to their canvas drawings
    """
    # debugging message
    logging.info("creating vents")
    # create the vents
    vent_objects = {}
    vent_drawings = {}
    for _ in range(n_vents):
        # save the vents using their memory id
        vent_object = vent.Vent(prod_rate=constants.VENT_PROD_RATE)
        vent_id = id(vent_object)
        vent_objects[vent_id] = vent_object
        # retrieve vent attributes
        position = vent_object.get_position()
        radius = vent_object.get_radius()
        color = vent_object.get_color()
        # draw the vents
        vent_drawing = utils.draw_circular_object(
            canvas=canvas,
            position=position,
            radius=radius,
            fill_color=color,
            outline_color=constants.VENT_OUTLINE_COLOR,
        )
        # save the vent drawing via its memory id
        vent_drawings[vent_id] = vent_drawing
    # update the canvas with the vents
    window.update()
    return (
        vent_objects,
        vent_drawings,
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
    # debugging message
    logging.info("moving cells")
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
    # debugging message
    logging.info("checking health of all cells and reaping where necessary")
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
    # update the window
    window.update()
    # return the new trackers
    return new_cell_objects, new_cell_drawings


def create_labels(window: tkinter.Tk):
    """
    creates statistic labels to display under the exit button

    @param window = tkinter window to create a canvas in and update
    @returns labels = map of labels with key being the title of each one
    """
    # debugging message
    logging.info("creating labels")
    # create tracker
    labels = {}
    # add the round label
    labels["rounds"] = tkinter.Label(window, text="0 rounds")
    labels["rounds"].grid(row=0, column=0, sticky=tkinter.NW)
    # add the n-cells label
    labels["cells"] = tkinter.Label(window, text="0 cells")
    labels["cells"].grid(row=1, column=0, sticky=tkinter.NW)
    return labels


def update_labels(window: tkinter.Tk, labels: Dict[str, tkinter.Label], n_cells: int):
    """
    updates the labels with new round numbers and new n-cells

    @param window = window labels reside in
    @param labels = map of labels with key being the title of each one
    @param n_cells = new number of cells present in the environment
    """
    # debugging message
    logging.info("updating labels")
    # get the current round number
    round_num = int(labels["rounds"]["text"].split(" ")[0])
    # update the round number
    labels["rounds"]["text"] = f"{round_num + 1} rounds"
    # update the number of cells
    labels["cells"]["text"] = f"{n_cells} cells"
    window.update()


def process_vents(
    window: tkinter.Tk,
    canvas: tkinter.Canvas,
    vent_objects: Dict,
    food_objects: Dict,
    food_drawings: Dict,
):
    """
    updates the food objects and drawings with the new foods from the vents

    @param window = window to draw on
    @param canvas = canvas to draw in
    @param vent_objects = vents to get data from
    @param food_objects = object tracker of food
    @param food_drawings = canvas drawing tracker of food
    """
    # debugging message
    logging.info("updating vents with new foods")
    # loop through the vents
    for _, vent_object in vent_objects.items():
        vent_food_objects, vent_food_drawings = vent_object.create_foods(canvas=canvas)
        food_objects.update(vent_food_objects)
        food_drawings.update(vent_food_drawings)
    window.update()


def calc_currents_flat(vent_objects: Dict) -> np.array:
    """
    computes the single digit resolution map of the currents
    based on the vents in the current system

    @param vent_objects = dictionary of vent objects to get their positions
    @returns currentx_map = currents with single number resolution for x axis
    @returns currenty_map = currents with single number resolution for y axis
    """
    # debugging message
    logging.info("beginning flat current calculations")
    # get vent positions
    tup = [vent_object.get_position() for vent_object in vent_objects.values()]
    vent_positions = np.vstack(tup=tup)
    # get vent radius as a function of power
    vent_radii = np.array([vent_obj.get_radius() for vent_obj in vent_objects.values()])
    # instantiate tracking variables
    currentx_map = np.zeros(shape=(constants.WINDOW_WIDTH, constants.WINDOW_HEIGHT))
    currenty_map = np.zeros(shape=(constants.WINDOW_WIDTH, constants.WINDOW_HEIGHT))
    # add in the current vent values
    for idx in range(currentx_map.shape[0]):
        for idy in range(currentx_map.shape[1]):
            # retrieve position
            position = np.array([idx, idy])
            # calculate difference from vents
            differences = vent_positions - position
            # calculate distances
            distances = np.linalg.norm(differences, axis=1)
            # calculate scaling factors
            scaling_factors = np.array([vent_radii / (distances + 1)]).T
            # calculate thetas
            thetas = np.arctan2(differences[:, 1], differences[:, 0])
            # use thetas to compute unit circle values
            unit_steps = np.vstack([np.cos(thetas), np.sin(thetas)]).T
            # finally compute the current, we take negative bc of backwards counting
            current = -(scaling_factors * unit_steps).sum(0) * constants.CURRENT_SCALER
            # save the currents
            currentx_map[idy, idx] = current[0]
            currenty_map[idy, idx] = current[1]
    return (currentx_map, currenty_map)


def calc_currents_round(vent_objects: Dict) -> np.array:
    """
    computes the single digit resolution map of the currents
    based on the vents in the current system assuming a circular world

    @param vent_objects = dictionary of vent objects to get their positions
    @returns currentx_map = currents with single number resolution for x axis
    @returns currenty_map = currents with single number resolution for y axis
    """
    # debugging message
    logging.info("beginning round earth current calculations")
    # get vent positions with triple 3 x 3 format
    def _adjust_position(vent_object: Dict, multiplier: Tuple[int]):
        # unpack multiplier
        multiplierx, multipliery = multiplier
        # instantiate tracker
        multiplied_positions = []
        # add y
        y = vent_object.get_position()[1] + multipliery * constants.WINDOW_HEIGHT
        multiplied_positions.append(y)
        # add x
        x = vent_object.get_position()[0] + multiplierx * constants.WINDOW_WIDTH
        multiplied_positions.append(x)
        # convert to numpy array
        return np.array(multiplied_positions)

    # define multipliers for the x belt
    multipliersx = ((0, 0), (0, 1), (0, 2))
    # compute the vent positions for the five tiles of the 3 x 3 grid
    tup = [
        _adjust_position(vent_object=vent_object, multiplier=multiplier)
        for multiplier in multipliersx
        for vent_object in vent_objects.values()
    ]
    vent_positionsx = np.vstack(tup=tup)
    # define multipliers for the y belt
    multipliersy = ((0, 0), (1, 0), (2, 0))
    # compute the vent positions for the five tiles of the 3 x 3 grid
    tup = [
        _adjust_position(vent_object=vent_object, multiplier=multiplier)
        for multiplier in multipliersy
        for vent_object in vent_objects.values()
    ]
    vent_positionsy = np.vstack(tup=tup)

    # get vent radius as a function of power three times for the + part of the 3 x 3 grid
    # split into the x belt and y belt
    vent_radii = np.array(
        [vent_obj.get_radius() for _ in range(3) for vent_obj in vent_objects.values()]
    )

    # instantiate tracking variables but create three times the actual size
    currentx_map = np.zeros(shape=(constants.WINDOW_HEIGHT, constants.WINDOW_WIDTH * 3))
    currenty_map = np.zeros(shape=(constants.WINDOW_HEIGHT * 3, constants.WINDOW_WIDTH))

    # add in the current vent x values
    for idy in range(currentx_map.shape[0]):
        for idx in range(currentx_map.shape[1]):
            # retrieve position
            position = np.array([idx, idy])
            # calculate difference from vents
            differencesx = vent_positionsx - position
            # calculate distances
            distancesx = np.linalg.norm(differencesx, axis=1)
            # calculate scaling factors
            scaling_factorsx = np.array([vent_radii / (distancesx + 1)]).T
            # calculate thetas
            thetasx = np.arctan2(differencesx[:, 1], differencesx[:, 0])
            # use thetas to compute unit circle values
            unit_stepsx = np.vstack([np.cos(thetasx), np.sin(thetasx)]).T
            # finally compute the current, we take negative bc of backwards counting
            currentx = (
                -(scaling_factorsx * unit_stepsx).sum(0) * constants.CURRENT_SCALER
            )
            # save the currents
            currentx_map[idy, idx] = currentx[0]
    # add in the current vent y values
    for idy in range(currenty_map.shape[0]):
        for idx in range(currenty_map.shape[1]):
            # retrieve position
            position = np.array([idx, idy])
            # calculate difference from vents
            differencesy = vent_positionsy - position
            # calculate distances
            distancesy = np.linalg.norm(differencesy, axis=1)
            # calculate scaling factors
            scaling_factorsy = np.array([vent_radii / (distancesy + 1)]).T
            # calculate thetas
            thetasy = np.arctan2(differencesy[:, 1], differencesy[:, 0])
            # use thetas to compute unit circle values
            unit_stepsy = np.vstack([np.cos(thetasy), np.sin(thetasy)]).T
            # finally compute the current, we take negative bc of backwards counting
            currenty = (
                -(scaling_factorsy * unit_stepsy).sum(0) * constants.CURRENT_SCALER
            )
            # save the currents
            currenty_map[idy, idx] = currenty[1]
    # subset to reality
    currentx_map = currentx_map[:, constants.WINDOW_WIDTH : constants.WINDOW_WIDTH * 2]
    currenty_map = currenty_map[
        constants.WINDOW_HEIGHT : constants.WINDOW_HEIGHT * 2, :
    ]
    # flip to what we want it to be indexed by x, y
    tmp_map = currentx_map.T
    currentx_map = currenty_map.T
    currenty_map = tmp_map
    return (currentx_map, currenty_map)


def calc_currents(vent_objects: Dict) -> np.array:
    """
    computes the single digit resolution map of the currents
    based on the vents in the current system with the constants world assumption

    @param vent_objects = dictionary of vent objects to get their positions
    @returns currentx_map = currents with single number resolution for x axis
    @returns currenty_map = currents with single number resolution for y axis
    """
    # debugging message
    logging.info("calculating currents depending on world type")
    # assuming a flat world
    if constants.WORLD_SHAPE == "flat":
        return calc_currents_flat(vent_objects=vent_objects)
    elif constants.WORLD_SHAPE == "round":
        return calc_currents_round(vent_objects=vent_objects)
    else:
        raise ValueError(f"constants.WORLD_SHAPE={constants.WORLD_SHAPE} is erroneous")


def diffuse_foods(
    window: tkinter.Tk,
    canvas: tkinter.Canvas,
    food_objects: Dict,
    food_drawings: Dict,
    currentx_map: np.array,
    currenty_map: np.array,
):
    """
    @param window = window to draw on
    @param canvas = canvas to draw in
    @param food_objects = food objects to get data from
    @param food_drawings = drawings to update
    @param currentx_map = currents to follow for axis x
    @param currenty_map = currents to follow for axis y
    """
    # debugging message
    logging.info("diffusing foods")
    # move each food
    for food_id, food_object in food_objects.items():
        # calculate the movement
        food_object.move(currentx_map=currentx_map, currenty_map=currenty_map)
        # retrieve food attributes
        position = food_object.get_position()
        radius = food_object.get_radius()
        food_drawing = food_drawings[food_id]
        # update the drawing
        utils.update_circular_object(
            canvas=canvas,
            position=position,
            radius=radius,
            drawing=food_drawing,
        )
    # update the window
    window.update()


def simulate_cells(
    window: tkinter.Tk,
    canvas: tkinter.Canvas,
    n_cells: int,
    n_vents: int,
    ideal_seqs: Dict[str, str],
):
    """
    creates cells and simulates their evolution and growth

    @param window = tkinter window to create a canvas in and update
    @param canvas = tkinter canvas to draw and manipulate objects in
    @param n_cells = number of cells to start with
    @param n_vents = number of vents to start with
    @param ideal_seqs = the idealized sequence to compare the cells with
    """
    # debugging message
    logging.info("beginning overall cell simulation")
    # instantiate the food objects
    food_objects = {}
    food_drawings = {}
    # create the vents
    vent_objects, vent_drawings = create_vents(
        window=window, canvas=canvas, n_vents=n_vents
    )
    # create the cells
    cell_objects, cell_drawings = create_cells(
        window=window, canvas=canvas, n_cells=n_cells, ideal_seqs=ideal_seqs
    )
    # create the labels
    labels = create_labels(window=window)
    # update the labels
    update_labels(window=window, labels=labels, n_cells=len(cell_objects))
    # take the initial snapshot
    snapshot.take_snapshot(cell_objects=cell_objects, labels=labels, overwrite=True)
    # calculate the currents
    currentx_map, currenty_map = calc_currents(vent_objects=vent_objects)
    # simulate their movement
    while True:
        # debugging message
        logging.info("beginning next round")
        # loop through the vents
        process_vents(
            window=window,
            canvas=canvas,
            vent_objects=vent_objects,
            food_objects=food_objects,
            food_drawings=food_drawings,
        )
        # process food diffusion
        diffuse_foods(
            window=window,
            canvas=canvas,
            food_objects=food_objects,
            food_drawings=food_drawings,
            currentx_map=currentx_map,
            currenty_map=currenty_map,
        )
        # move the cells and update the objects
        move_cells(
            window=window,
            canvas=canvas,
            cell_objects=cell_objects,
            cell_drawings=cell_drawings,
        )
        # kill the cells if needed
        cell_objects, cell_drawings = reap_cells(
            window=window,
            canvas=canvas,
            cell_objects=cell_objects,
            cell_drawings=cell_drawings,
        )
        # update the labels
        update_labels(window=window, labels=labels, n_cells=len(cell_objects))
        # take the general snapshot if there are cells
        if len(cell_objects) > 0:
            snapshot.take_snapshot(
                cell_objects=cell_objects, labels=labels, overwrite=False
            )
        # pause between rounds
        time.sleep(constants.ROUND_SLEEP)

import os
import numpy as np
import source.constants as constants
from typing import Dict, Optional, List, Tuple
import tkinter
import logging

# generate a random genome
def gen_genome(
    size: Optional[int] = None,
    nucs: Optional[List[str]] = None,
    rng: Optional[np.random._generator.Generator] = None,
) -> str:
    """
    generates a random genome with a supplied size or
    defaults to parameters as defined by constants

    @param size = optional parameter of the size of the genome to create
    @param nucs = nucleotides to utilize defaults to those in constants
    @param rng = random number generator to create the genome
    @returns genome = string of the genome made of the allowed nucs
    """
    # configure parameters
    size = constants.DEFAULT_GENOME_SIZE if size is None else size
    nucs = constants.DEFAULT_NUCS if nucs is None else nucs
    rng = constants.DEFAULT_RNG if rng is None else rng
    # compute genome
    genome = "".join(rng.choice(nucs, size=size, replace=True))
    return genome


# generate a random frame for a trait
def gen_frame(
    size: int, rng: Optional[np.random._generator.Generator] = None
) -> List[int]:
    """
    generates a random frame for a given trait
    the max value that it can be is size
    it is a uniform distribution from 0

    @param size = max value to sample
    @param rng = random number generator to sample using
    @returns frame = start and end to sample for this gene
    """
    # configure parameters
    rng = constants.DEFAULT_RNG if rng is None else rng
    # compute frame
    idxs = rng.integers(low=0, high=size, endpoint=True, size=2)
    frame = (min(idxs), max(idxs))
    return frame


# generate a mutation type
def gen_mut_type(
    threshold: float, rng: Optional[np.random._generator.Generator] = None
) -> Optional[str]:
    """
    generate a mutation type based on the chance of overcoming
    the given threshold if it passes a threshold
    there is a defined chance of the mutation being an indel or a sub
    """
    # configure parameters
    rng = constants.DEFAULT_RNG if rng is None else rng
    # choose mutation
    is_mut = rng.uniform(low=0, high=1, size=1) < threshold
    if is_mut:
        rand_value = rng.uniform(low=0, high=1, size=1)
        # equal chance of ins and del
        if rand_value < constants.INDEL_THRESHOLD / 2:
            return "ins"
        elif rand_value < constants.INDEL_THRESHOLD:
            return "del"
        else:
            return "sub"
    else:
        return None


# generate a substitution
def gen_mut_sub(
    curr_nuc: str, rng: Optional[np.random._generator.Generator] = None
) -> str:
    """
    generate a substitution for the nucleotide

    @returns nuc = nucleotide
    """
    # configure parameters
    rng = constants.DEFAULT_RNG if rng is None else rng
    # choose nucleotide
    nucs = [nuc for nuc in constants.DEFAULT_NUCS if nuc != curr_nuc]
    nuc = rng.choice(nucs, size=1)[0]
    return nuc


# generate an insertion
def gen_mut_ins(rng: Optional[np.random._generator.Generator] = None) -> str:
    """
    generates an insertion basically a random nucleotide

    @returns nuc = nucleotide
    """
    # configure parameters
    rng = constants.DEFAULT_RNG if rng is None else rng
    # choose nucleotide
    nuc = rng.choice(constants.DEFAULT_NUCS, size=1)[0]
    return nuc


# generate a mutation
def gen_mut(
    threshold: float,
    curr_nuc: str,
    rng: Optional[np.random._generator.Generator] = None,
) -> Optional[str]:
    """
    generates a mutation based on a threshold and supplies
    the nucleotide that should be put into the new genome

    @param threshold = mutational threshold
    @param curr_nuc = the current nucleotide
    @param rng = random number generator
    @returns nuc = if needed it will generate a nucleotide
    """
    # configure parameters
    rng = constants.DEFAULT_RNG if rng is None else rng
    # generate mutation
    mut_type = gen_mut_type(threshold=threshold, rng=rng)
    if mut_type == "sub":
        return gen_mut_sub(curr_nuc=curr_nuc, rng=rng)
    elif mut_type == "ins":
        return curr_nuc + gen_mut_ins(rng=rng)
    elif mut_type == "del":
        return ""
    else:
        return curr_nuc


# generate the mutate frame for a start or end
def gen_mut_frame(
    value: int, threshold: int, rng: Optional[np.random._generator.Generator] = None
) -> int:
    """
    generates the mutated value for a frame based on its mutation rate

    @param value = current frame value
    @param threshold = mutational trait threshold
    @param rng = random number generator
    @returns new mutated frame value or previous value if no mutation
    """
    # configure parameters
    rng = constants.DEFAULT_RNG if rng is None else rng
    # get mutated value or return original
    is_mut = rng.uniform(low=0, high=1, size=1) < threshold
    if is_mut:
        delta = rng.normal(loc=0, scale=threshold * constants.FRAME_STD_MAX, size=1)[0]
        return value + round(delta)
    else:
        return value


# scale the steps to a given magnitude
def calc_scaling_factor(magnitude: float) -> List[float]:
    """
    calculates the scaling factor for the given magnitude

    @param magnitude = the total distance the steps should equate to
    @returns scaled_rand_steps = random steps scaled to a given magnitude
    """
    # only proceed if magnitude > 0
    if magnitude == 0:
        return np.nan
    # convert the steps to float type
    steps = np.array([constants.STEP_RESOLUTION] * 2, dtype=float)
    # calculate the scaling factor to scale the random steps by
    # the calculation is based on reversing L2 norm (i.e. euclidean distance)
    # A^2 + B^2 = C^2 and we have (A'/F)^2 + (B'/F)^2 = C^2
    # we're trying to solve for F, we abstract to SUM((STEP/F)^2 for each STEP) = C^2
    # thus we solve for F via the idea that (X/Y)^2 = X^2 * (1/Y)^2
    # so C^2 = 1/F^2 * SUM(STEP^2 for each STEP)
    # thus F^2 = SUM(STEP^2 for each STEP) / C^2
    # giving us F = SQRT( SUM( STEP^2 for each STEP ) / C^2 )
    scaling_factor = np.sqrt(np.power(steps, 2).sum() / np.power(magnitude, 2))
    return scaling_factor


# generate deltas for the cells movements
def gen_deltas(
    scaling_factor: float, rng: Optional[np.random._generator.Generator] = None
) -> List[float]:
    """
    generates random steps then scales it to the given scaling factor
    which scales it to the max step that this given cell can take

    @param scaling_factor = the dividing factor for the cell's max magnitude
    @param rng = random number generator
    @returns scaled_rand_steps = random steps scaled to a given magnitude
    """
    # only proceed if scaling factor is not derived from a magnitude = 0
    if scaling_factor == np.nan:
        return np.zeros(shape=rand_steps.shape)
    # configure parameters
    rng = constants.DEFAULT_RNG if rng is None else rng
    # generate the random integer steps
    rand_steps = rng.integers(-constants.STEP_RESOLUTION, constants.STEP_RESOLUTION, 2)
    # only proceed if there is movement
    if rand_steps.sum() == 0:
        return rand_steps
    # scale the steps
    scaled_rand_steps = rand_steps / scaling_factor
    return scaled_rand_steps


# calculate corners from center and radius
def calc_corner_coords(position: List[float], radius: float) -> Tuple[float]:
    """
    derives corners from an object's position and radius

    @param position = center of the object
    @param radius = radius of the object
    @returns corners = as [top left x, top left y, bottom right x, bottom right y]
    """
    # unpack the position
    x, y = position
    # derive the corner coordinates
    tl_x, tl_y = x - radius, y - radius
    br_x, br_y = x + radius, y + radius
    return (tl_x, tl_y, br_x, br_y)


# draw the oval given it's position and radius
def draw_circular_object(
    canvas: tkinter.Canvas,
    position: List[float],
    radius: float,
    fill_color: str = None,
    outline_color: str = None,
):
    """
    draws a circular object on the given canvas of dimensions provided

    @param canvas = tkinter canvas to draw on
    @param position = center of the object
    @param radius = radius of the object
    @param fill_color = color of the inside of the circular object
    @param outline_color = color outlining the circular object
    @returns drawing = canvas drawing of the object
    """
    # configure parameters
    fill_color = constants.DEFAULT_FILL_COLOR if fill_color is None else fill_color
    outline_color = (
        constants.DEFAULT_OUTLINE_COLOR if outline_color is None else outline_color
    )
    # calculate the corner coordinates
    tl_x, tl_y, br_x, br_y = calc_corner_coords(position=position, radius=radius)
    # draw the cell on the canvas
    drawing = canvas.create_oval(
        tl_x, tl_y, br_x, br_y, fill=fill_color, outline=outline_color
    )
    return drawing


# update the oval given it's position and radius
def update_circular_object(
    canvas: tkinter.Canvas,
    position: List[float],
    radius: float,
    drawing,
):
    """
    updates a circular object on the given canvas of dimensions provided

    @param canvas = tkinter canvas to draw on
    @param position = center of the object
    @param radius = radius of the object
    @param drawing = the original drawing
    @returns drawing = new canvas drawing of the object
    """
    # calculate the corner coordinates
    tl_x, tl_y, br_x, br_y = calc_corner_coords(position=position, radius=radius)
    # draw the cell on the canvas
    canvas.coords(drawing, tl_x, tl_y, br_x, br_y)


# generate a random color
def gen_color(rng: Optional[np.random._generator.Generator] = None) -> str:
    """
    generates a random color

    @param rng = random number generator to create the genome
    @returns hex_color = string of the hex color
    """
    # configure parameters
    rng = constants.DEFAULT_RNG if rng is None else rng
    # define method to generate random rgb value
    rand_rgb = lambda: rng.integers(0, 256)
    # create hex color %02X means convert to hexadecimal format
    hex_color = "#%02X%02X%02X" % (rand_rgb(), rand_rgb(), rand_rgb())
    return hex_color


# create a directory if it does not exist
def create_dir_if_none(dirname: str, overwrite: bool):
    """
    creates a directory if none exist, if one exists it returns 2
    if none exists than it creates one and returns 0 if any errors are
    returned then it returns 1 and logs the error

    @param dirname = name of the directory to create
    @param overwrite = whether or not to remove the directory prior
    @returns status code
    """
    # remove if needed
    if overwrite:
        os.system(f"rm -rf {dirname}")
    # skip if the directory already exists
    if os.path.exists(dirname):
        return 2
    # else create the directory
    try:
        os.mkdir(dirname)
        return 0
    # catch any errors that are thrown
    except Exception as e:
        logging.exception(f"[create_dir_if_none] threw {str(e)}")
        return 1


# generates a random position on the map
def gen_position(rng: Optional[np.random._generator.Generator] = None) -> np.array:
    """
    generates a random position on the window

    @param rng = random number generator to create the genome
    @returns position = numpy array of the random coordinates
    """
    # configure parameters
    rng = constants.DEFAULT_RNG if rng is None else rng
    # retrieve the indexes for x and y axes
    idx = rng.uniform(0, constants.WINDOW_WIDTH)
    idy = rng.uniform(0, constants.WINDOW_HEIGHT)
    # combine into a position
    position = np.array([idx, idy])
    return position


# generates a number from a specified distribution
def gen_distribution(
    distribution: str,
    kwargs: Dict,
    rng: Optional[np.random._generator.Generator] = None,
) -> float:
    """
    generates a number from a given distribution

    @param distribution = name of the distribution to utilize
    @param kwargs = any other key word arguments to be inputted to distributions
    @returns number = number randomly selected from distribution
    """
    # configure parameters
    rng = constants.DEFAULT_RNG if rng is None else rng
    # default number to 0
    number = 0
    # service uniform
    if distribution == "uniform":
        # utilizes `low`, `high`
        number = rng.uniform(low=kwargs["low"], high=kwargs["high"], size=1)[0]
    # service normal
    elif distribution == "normal":
        # utilizes `loc`, `scale`
        number = rng.normal(loc=kwargs["loc"], scale=kwargs["scale"], size=1)[0]
    # service bimodal
    elif distribution == "bimodal":
        # decided if it is right or left
        is_left = rng.uniform(low=0, high=1) >= 0.5
        if is_left:
            # utilizes `loc`, `scale`
            number = rng.normal(loc=kwargs["loc1"], scale=kwargs["scale1"], size=1)[0]
        else:
            # utilizes `loc`, `scale`
            number = rng.normal(loc=kwargs["loc2"], scale=kwargs["scale2"], size=1)[0]
    return number


# set limits on the given data
def limit_input(number: float, vmin: float, vmax: float) -> float:
    """
    limits the given number to vmin and vmax

    @param number = the number to correct
    @param vmin = the minimum value the number can be
    @param vmax = the maximum value the number can be
    @returns the limited number post correction
    """
    # fix the number if it is smaller
    limited_number = number
    # keep looping until the number is perfect for example
    # vmin = -5, vmax = 5, number = -50 then it'll cycle to 5 - (-5 -- 50)
    # which gets us 5 - 45 = -40 this will continue to cycle to 0
    while limited_number < vmin or limited_number > vmax:
        # if the number is too small calculate the difference and
        # subtract it from the max to get the new value
        if limited_number < vmin:
            limited_number = vmax - (vmin - limited_number)
        # if the number is too large then calculate the difference and
        # add the overhead to the minimum to get the new value
        elif limited_number > vmax:
            limited_number = vmin + (limited_number - vmax)
        # this should never happen but if it is equal then leave the loop
        else:
            break
    return limited_number

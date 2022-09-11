from turtle import pos
import numpy as np
import source.constants as constants
from typing import Optional, List, Tuple

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


# generate step for cells to take
# TODO: scale to multiple dimensions but for now assume two dimensions
def gen_rand_steps(rng: Optional[np.random._generator.Generator] = None) -> List[int]:
    """
    generates steps in a random direction in an object's given dimension

    @param rng = random number generator
    @returns rand_steps = numpy array of the random non-scaled steps
    """
    # configure parameters
    rng = constants.DEFAULT_RNG if rng is None else rng
    # generate the random integer steps
    rand_steps = rng.integers(-constants.STEP_RESOLUTION, constants.STEP_RESOLUTION, 2)
    return rand_steps


# scale the steps to a given magnitude
def scale_rand_steps(magnitude: float, rand_steps: List[int]) -> List[float]:
    """
    scales the random steps by the given magnitude

    @param magnitude = the total distance the steps should equate to
    @returns scaled_rand_steps = random steps scaled to a given magnitude
    """
    # only proceed if magnitude > 0
    if magnitude == 0:
        return np.zeros(shape=rand_steps.shape)
    # only proceed if there is movement
    if rand_steps.sum() == 0:
        return rand_steps
    # convert the random steps to float type
    rand_steps = rand_steps.astype(float)
    # calculate the scaling factor to scale the random steps by
    # the calculation is based on reversing L2 norm (i.e. euclidean distance)
    # A^2 + B^2 = C^2 and we have (A'/F)^2 + (B'/F)^2 = C^2
    # we're trying to solve for F, we abstract to SUM((STEP/F)^2 for each STEP) = C^2
    # thus we solve for F via the idea that (X/Y)^2 = X^2 * (1/Y)^2
    # so C^2 = 1/F^2 * SUM(STEP^2 for each STEP)
    # thus F^2 = SUM(STEP^2 for each STEP) / C^2
    # giving us F = SQRT( SUM( STEP^2 for each STEP ) / C^2 )
    scaling_factor = np.sqrt(np.power(rand_steps, 2).sum() / np.power(magnitude, 2))
    # scale by the scaling factor
    scaled_rand_steps = rand_steps / scaling_factor
    return scaled_rand_steps


# generate deltas using the above two functions
def gen_deltas(
    magnitude: float, rng: Optional[np.random._generator.Generator] = None
) -> List[float]:
    """
    generates random steps then scales it to the given magnitude

    @param magnitude = the total distance the steps should equate to
    @param rng = random number generator
    @returns scaled_rand_steps = random steps scaled to a given magnitude
    """
    # calculate random steps
    rand_steps = gen_rand_steps(rng=rng)
    # scale random steps
    scaled_rand_steps = scale_rand_steps(magnitude=magnitude, rand_steps=rand_steps)
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


# draw the cell given it's position and radius
def draw_circular_object(
    canvas,
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

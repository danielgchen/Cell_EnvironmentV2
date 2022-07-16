import numpy as np
import constants
from typing import Optional, List

# generate a random genome
def gen_genome(
    size: Optional[int] = None,
    nucs: Optional[List[str]] = None,
    rng: Optional[np.random._generator.Generator] = None
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
    size: int,
    rng: Optional[np.random._generator.Generator] = None
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
import numpy as np
import constants
from typing import Optional, List

# generate a random genome
def gen_rand_genome(
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
    # define tracking string
    return "".join(rng.choice(nucs, size=size, replace=True))

print(gen_rand_genome())

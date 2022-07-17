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

# generate a mutation type
def gen_mut_type(
    threshold: float,
    rng: Optional[np.random._generator.Generator] = None
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
    curr_nuc: str,
    rng: Optional[np.random._generator.Generator] = None
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
def gen_mut_ins(
    rng: Optional[np.random._generator.Generator] = None
) -> str:
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
    rng: Optional[np.random._generator.Generator] = None
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
    value: int,
    threshold: int,
    rng: Optional[np.random._generator.Generator] = None
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
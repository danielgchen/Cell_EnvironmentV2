import numpy as np

# nucleotides in the genome
DEFAULT_NUCS = ["A","C","G","T"]
# size of the genome to create
DEFAULT_GENOME_SIZE = 10
# random number generator
DEFAULT_RNG = np.random.default_rng(0)

# cell traits
CELL_TRAITS = ["digest", "move", "mutate"]

# environment genetic optimals
DIGEST_SIZE = 20
MOVE_SIZE = 20
MUTATE_SIZE = 5
import numpy as np

# nucleotides in the genome
DEFAULT_NUCS = ["A", "C", "G", "T"]
# size of the genome to create
DEFAULT_GENOME_SIZE = 115
# random number generator
DEFAULT_RNG = np.random.default_rng(0)
# chance for a mutation to be an indel
INDEL_THRESHOLD = 0.1

# cell traits
CELL_TRAITS = ["digest", "move", "mutate"]
# frame mutation components
FRAME_MUT_PERC_OF_GENOME = 0.2
FRAME_STD_MAX = round(DEFAULT_GENOME_SIZE * FRAME_MUT_PERC_OF_GENOME)

# environment genetic optimals
DIGEST_SIZE = 50
MOVE_SIZE = 50
MUTATE_SIZE = 15

# window parameters
WINDOW_NAME = "Cell Modeling Environment"
WINDOW_WIDTH = WINDOW_HEIGHT = 500
BKGD_COLOR = "#ffffff"

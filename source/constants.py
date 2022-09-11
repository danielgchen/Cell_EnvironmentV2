import numpy as np

# window parameters
WINDOW_NAME = "Cell Modeling Environment"
WINDOW_WIDTH = WINDOW_HEIGHT = 500
BKGD_COLOR = "#ffffff"

# nucleotides in the genome
DEFAULT_NUCS = ["A", "C", "G", "T"]
# size of the genome to create
DEFAULT_GENOME_SIZE = 115
# random number generator
DEFAULT_RNG = np.random.default_rng(0)
# chance for a mutation to be an indel
INDEL_THRESHOLD = 0.1
# movement resolutions
STEP_RESOLUTION = 4

# cell traits
CELL_TRAITS = ["digest", "move", "mutate"]
# frame mutation components
FRAME_MUT_PERC_OF_GENOME = 0.2
FRAME_STD_MAX = round(DEFAULT_GENOME_SIZE * FRAME_MUT_PERC_OF_GENOME)
# movement components
MOVE_WINDOW_WIDTH_PERC = 0.01
MOVE_STEP_SIZE = WINDOW_WIDTH * MOVE_WINDOW_WIDTH_PERC
# energy components
ENERGY_WINDOW_WIDTH_PERC = 0.1
INITIAL_ENERGY = round(ENERGY_WINDOW_WIDTH_PERC / MOVE_WINDOW_WIDTH_PERC)

# environment genetic optimals
DIGEST_SIZE = 50
MOVE_SIZE = 50
MUTATE_SIZE = 15

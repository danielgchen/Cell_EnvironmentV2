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
# position components
WINDOW_WIDTH_CENTER = WINDOW_WIDTH / 2
WINDOW_HEIGHT_CENTER = WINDOW_HEIGHT / 2
INITIAL_POSITION = np.array([WINDOW_WIDTH_CENTER, WINDOW_HEIGHT_CENTER])
# movement components
MOVE_WINDOW_WIDTH_PERC = 0.01
MOVE_STEP_SIZE = WINDOW_WIDTH * MOVE_WINDOW_WIDTH_PERC
# energy components
ENERGY_WINDOW_WIDTH_PERC = 0.50
INITIAL_ENERGY = round(ENERGY_WINDOW_WIDTH_PERC / MOVE_WINDOW_WIDTH_PERC)
# radius components
CELL_RADIUS_WIDTH_PERC = 0.025
CELL_RADIUS = WINDOW_WIDTH * CELL_RADIUS_WIDTH_PERC
# color components
CELL_OUTLINE_COLOR = "maroon"

# environment genetic optimals
DIGEST_SIZE = 50
MOVE_SIZE = 50
MUTATE_SIZE = 15
# colors
DEFAULT_FILL_COLOR = "#ffffff"
DEFAULT_OUTLINE_COLOR = "#000000"

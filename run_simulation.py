import environment
import argparse

"""
this program represents genetic development of a randomized subset of cells
it creates idealized genomic sequences for a set of genes and the cells
are graded against these idealized sequences, those cells that do better
are kept and are allowed to replicate and mutate, mutated children
are then filtered based on their new scores against the ideal sequences
this is continue for `perc_res` number of steps and typically with enough
steps and enough children reaches a perfect match against the idealized genomes
"""

# define argument parser
parser = argparse.ArgumentParser()
parser.add_argument(
    "--n-cells", type=int, default=5, help="number of cells to start with"
)
parser.add_argument(
    "--perc-res", type=int, default=200, help="the number of steps to take"
)
parser.add_argument(
    "--n-children",
    type=int,
    default=2000,
    help="the number of children each cell produces",
)
parser.add_argument(
    "--n-filter",
    type=int,
    default=200,
    help="sthe number of children to filter down to",
)

# parse the arguments
args = parser.parse_args()

# create the idealized sequences
ideal_seqs = environment.create_ideal_seqs()

# run the simulation
environment.simulate_cells(
    n_cells=args.n_cells,
    perc_res=args.perc_res,
    n_children=args.n_children,
    n_filter=args.n_filter,
    ideal_seqs=ideal_seqs,
)

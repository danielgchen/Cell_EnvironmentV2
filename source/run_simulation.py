import source.environment as environment

"""
this program represents genetic development of a randomized subset of cells
it creates idealized genomic sequences for a set of genes and the cells
are graded against these idealized sequences, those cells that do better
are kept and are allowed to replicate and mutate, mutated children
are then filtered based on their new scores against the ideal sequences
this is continue for `perc_res` number of steps and typically with enough
steps and enough children reaches a perfect match against the idealized genomes
"""

def run_simulation(
    n_cells: int = 5,
    perc_res: int =200,
    n_children: int = 2000,
    n_filter: int = 200,
):
    """
    implementation of the program described above

    @param n_cells = number of cells to start with
    @param perc_res = the number of steps to take
    @param n_children = the number of children each cell produces
    @param n_filter = the number of children to filter down to
    """
    # create the idealized sequences
    ideal_seqs = environment.create_ideal_seqs()

    # create the window and canvas
    window, canvas = environment.create_canvas()

    # run the simulation
    environment.simulate_cells(
        n_cells=n_cells,
        perc_res=perc_res,
        n_children=n_children,
        n_filter=n_filter,
        ideal_seqs=ideal_seqs,
    )

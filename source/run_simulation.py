import source.environment as environment

"""
this program represents genetic development of a randomized subset of cells
it creates idealized genomic sequences for a set of genes and the cells
are graded against these idealized sequences, these grades roughly translate
into overall fitness which allows them to reproduce, cells reproduce
mitotically and accumulate mutations throughout their lifespan until death,
where death is defined by the loss of all energy and biologic sustainability
"""

def run_simulation(
    n_cells: int = 5,
):
    """
    implementation of the program described above

    @param n_cells = number of cells to start with
    """
    # create the idealized sequences
    ideal_seqs = environment.create_ideal_seqs()

    # create the window and canvas
    window, canvas = environment.create_canvas()

    # run the simulation
    environment.simulate_cells(
        n_cells=n_cells,
        ideal_seqs=ideal_seqs,
    )

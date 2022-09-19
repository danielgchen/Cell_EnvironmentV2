import tkinter
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
    n_cells: int = 1,
):
    """
    implementation of the program described above

    @param n_cells = number of cells to start with
    """
    # create the idealized sequences
    ideal_seqs = environment.create_ideal_seqs()

    # create the window and canvas
    window, canvas = environment.create_canvas()

    # add exit button to stop the loop
    exit_button = tkinter.Button(
        window,
        text="Exit!",
        width=2,
        height=1,
        command=window.destroy,
    )
    exit_button.grid(row=2, column=1, sticky=tkinter.SE)

    # run the simulation
    environment.simulate_cells(
        window=window,
        canvas=canvas,
        n_cells=n_cells,
        ideal_seqs=ideal_seqs,
    )

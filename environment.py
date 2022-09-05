import utils
import constants
import cell
from typing import Dict

# define ideal sequences
def create_ideal_seqs():
    """
    instantiates ideal sequences based on gene sizes defined in constants

    @returns ideal_seqs = idealized sequences that are randomly generated
    """
    ideal_seqs = {
        "digest": utils.gen_genome(size=constants.DIGEST_SIZE),
        "move": utils.gen_genome(size=constants.MOVE_SIZE),
        "mutate": utils.gen_genome(size=constants.MUTATE_SIZE)
    }
    return ideal_seqs


# create cells
def simulate_cells(
    n_cells: int,
    perc_res: int,
    n_children: int,
    n_filter: int,
    ideal_seqs: Dict[str, str]
):
    """
    creates cells and simulates their evolution and reports their growth

    @param n_cells = number of cells to start with
    @param perc_res = the number of steps to take
    @param n_children = the number of children each cell produces
    @param n_filter = the number of children to filter down to
    @param ideal_seqs = the idealized sequence to compare the cells with
    """
    # create the cells
    cells = [cell.Cell(traits=constants.CELL_TRAITS, ideal_seqs=ideal_seqs) for _ in range(n_cells)]
    for perc in range(perc_res):
        print(f"now filtering for {perc / perc_res}...")
        # mutate this round
        new_cells = []
        for obj in cells:
            digest = obj.get_trait_score(trait="digest")
            move = obj.get_trait_score(trait="move")
            if digest > perc / perc_res and move > perc / perc_res:
                # report passing cells
                new_cells.append((obj, digest, move))
                # mutate the cell
                for _ in range(n_children):
                    # prepare cell attributes
                    kwargs = obj.mut_self()
                    kwargs["traits"] = obj.get_traits()
                    kwargs["ideal_seqs"] = ideal_seqs
                    mut_obj = cell.Cell(**kwargs)
                    mut_digest = mut_obj.get_trait_score(trait="digest")
                    mut_move = mut_obj.get_trait_score(trait="move")
                    if mut_digest > perc / perc_res and mut_move > perc / perc_res:
                        new_cells.append((mut_obj, mut_digest, mut_move))
        
        # sort the passing cells by both digestion and moving
        new_cells = sorted(new_cells, key=lambda row: row[1] + row[2], reverse=True)
        # add on the diverse genomes of passing cells
        # instantiate new tracker of the cells and genomes utilized
        cells = []
        genomes = {"digest":[], "move":[]}
        idx = 0
        # keep working through cells as long as there are cells to filter
        while len(cells) < n_filter and idx < len(new_cells):
            # grab the cell
            obj = new_cells[idx][0]
            # get it's genome
            genome = obj.get_genome()
            unique = True
            # mutate each trait
            for trait in ["digest", "move"]:
                start, end = obj.get_trait_frame(trait=trait)
                if genome[start:end] in genomes[trait]:
                    unique = False
                    pass
                else:
                    genomes[trait].append(genome[start:end])
            # only add the cell if it mutated a unique genome
            if unique:
                cells.append(obj)
            idx += 1
        # print the number of remaining cells
        print(f"filtered to {len(cells)} cells")
        del new_cells

        # report the cells
        for obj in cells:
            # complete this for digest and move
            for trait in ["digest", "move"]:
                start, end = obj.get_trait_frame(trait=trait)
                # print out the round and trait informaiton
                print(f">round_{perc}", start, end, 
                    f"{trait}={round(obj.get_trait_score(trait=trait), 4)}",
                    obj.get_genome()[start:end])
                # print out the current length of the genome and the genome
                print(len(obj.get_genome()), obj.get_genome())
        # print out a new line
        print()

    # print out the ideal sequence
    print(ideal_seqs)
import utils
import constants
import cell

# define ideal sequences
IDEAL_SEQS = {
    "digest": utils.gen_genome(size=constants.DIGEST_SIZE),
    "move": utils.gen_genome(size=constants.MOVE_SIZE),
    "mutate": utils.gen_genome(size=constants.MUTATE_SIZE)
}

# create cells
cells = [cell.Cell(traits=constants.CELL_TRAITS, ideal_seqs=IDEAL_SEQS) for _ in range(5)]
perc_res = 10
n_children = 100
for perc in range(perc_res):
    print(f"now filtering for {perc / perc_res}...")
    # mutate this round
    new_cells = []
    results = []
    for obj in cells:
        start, end = obj.get_trait_frame(trait="digest")
        if obj.get_trait_score(trait="digest") > perc / perc_res:
            # report passing cells
            new_cells.append((obj, obj.get_trait_score(trait="digest")))
            # mutate the cell
            for _ in range(n_children):
                # prepare cell attributes
                kwargs = obj.mut_self()
                kwargs["traits"] = obj.get_traits()
                kwargs["ideal_seqs"] = IDEAL_SEQS
                mut_obj = cell.Cell(**kwargs)
                new_cells.append((mut_obj, mut_obj.get_trait_score(trait="digest")))
    # reset with the passing cells
    new_cells = sorted(new_cells, key=lambda row: row[1], reverse=True)
    cells = [row[0] for row in new_cells[:10]]
    del new_cells
    for obj in cells:
        start, end = obj.get_trait_frame(trait="digest")
        print(f">round_{perc}")
        print(obj.get_genome()[start:end])
        print()
    for obj in cells:
        print(round(obj.get_trait_score(trait="digest"), 4))
    print()

print(IDEAL_SEQS)
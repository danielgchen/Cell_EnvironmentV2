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
perc_res = 200
n_children = 2000
n_filter = 200
for perc in range(perc_res):
    print(f"now filtering for {perc / perc_res}...")
    # mutate this round
    new_cells = []
    results = []
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
                kwargs["ideal_seqs"] = IDEAL_SEQS
                mut_obj = cell.Cell(**kwargs)
                mut_digest = mut_obj.get_trait_score(trait="digest")
                mut_move = mut_obj.get_trait_score(trait="move")
                if mut_digest > perc / perc_res and mut_move > perc / perc_res:
                    new_cells.append((mut_obj, mut_digest, mut_move))
    # sort the passing cells by both digestion and moving
    new_cells = sorted(new_cells, key=lambda row: row[1] + row[2], reverse=True)
    # add on the diverse genomes of passing cells
    cells = []
    genomes = {"digest":[], "move":[]}
    idx = 0
    while len(cells) < n_filter and idx < len(new_cells):
        obj = new_cells[idx][0]
        genome = obj.get_genome()
        unique = True
        for trait in ["digest", "move"]:
            start, end = obj.get_trait_frame(trait=trait)
            if genome[start:end] in genomes[trait]:
                unique = False
                pass
            else:
                genomes[trait].append(genome[start:end])
        if unique:
            cells.append(obj)
        idx += 1
    print(f"filtered to {len(cells)} cells")
    del new_cells
    for obj in cells:
        # complete this for digest and move
        for trait in ["digest", "move"]:
            start, end = obj.get_trait_frame(trait=trait)
            print(f">round_{perc}", start, end, 
                  f"{trait}={round(obj.get_trait_score(trait=trait), 4)}",
                  obj.get_genome()[start:end])
            print(len(obj.get_genome()), obj.get_genome())
    print()

print(IDEAL_SEQS)
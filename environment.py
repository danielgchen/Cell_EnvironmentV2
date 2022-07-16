import utils
import constants
import cell

# define ideal sequences
IDEAL_SEQS = {
    "digest": utils.gen_genome(size=constants.DIGEST_SIZE),
    "move": utils.gen_genome(size=constants.MOVE_SIZE),
    "mutate": utils.gen_genome(size=constants.MUTATE_SIZE)
}
print(IDEAL_SEQS)

# create cells
cell = cell.Cell()
print(cell.get_genome())
for trait in cell.get_traits():
    cell.calc_trait_score(trait=trait, ideal_seq=IDEAL_SEQS[trait])
    print(cell.get_trait_frame(trait=trait))
    print(cell.get_trait_score(trait=trait))
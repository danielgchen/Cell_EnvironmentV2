import unittest
import source.cell as cell


class CellTests(unittest.TestCase):
    # set up the cell for testing
    def setUp(self) -> None:
        # define ideal sequences
        self.ideal_seqs = {"mutate": "AAACCCTTTGGG", "b": "AACCTTGG", "c": "ACTG"}
        # define traits
        self.traits = ["mutate", "b", "c"]
        # define traits to frame
        self.trait2frame = {"mutate": (0, 10), "b": (10, 20), "c": (20, 30)}
        # define genome
        self.genome = "AAACCCTTTGGGAAACCCTTTGGGAACCTTGGAACCTTGGACTGACTG"
        # define the cell
        self.cell = cell.Cell(
            ideal_seqs=self.ideal_seqs,
            traits=self.traits,
            trait2frame=self.trait2frame,
            genome=self.genome,
        )
        # define the expected genome size
        self.genome_size = 48
        # define the expected trait scores
        self.trait2score = {"mutate": 0.8333333333333334, "b": 0.25, "c": 0}
        # define the expected mutated genome
        self.mut_genome = "GGACCTACAGTTTCTATGGAAAATATTGTCTGAGATAAGAATTACGTC"
        # define the expected mutate trait frame
        self.mut_frame_trait = "mutate"
        self.mut_frame_trait_frame = (-3, 12)
        # define the expected mutate self result
        self.mut_self_kwargs = {
            "genome": "ATTCCAACTGACAGGAATAAGGACTGTCAGGGTCTCCGCGGATCAAGGA",
            "trait2frame": {"mutate": (21, 44), "b": (9, 21), "c": (-9, 79)},
        }
        # define inputs for calc_trait_score testing
        self.calc_trait_score_trait = "mutate"
        self.calc_trait_score_ideal_seq = "AAAAAAAA"
        self.calc_trait_score_trait_score = 0.125
        # define the expected move step size
        self.move_step_size = 5

    # test calculation functions
    def test_calc_trait_score(self) -> None:
        self.cell.calc_trait_score(
            trait=self.calc_trait_score_trait, ideal_seq=self.calc_trait_score_ideal_seq
        )
        trait_score = self.cell.get_trait_score(trait=self.calc_trait_score_trait)
        self.assertEqual(trait_score, self.calc_trait_score_trait_score)

    # test mutation functions
    def test_mut_genome(self) -> None:
        mut_genome = self.cell.mut_genome()
        self.assertEqual(mut_genome, self.mut_genome)

    def test_mut_frame(self) -> None:
        mut_frame = self.cell.mut_frame(trait=self.mut_frame_trait)
        self.assertEqual(mut_frame, self.mut_frame_trait_frame)

    def test_mut_self(self) -> None:
        kwargs = self.cell.mut_self()
        self.assertEqual(kwargs, self.mut_self_kwargs)

    # test get functions
    def test_genome(self) -> None:
        genome = self.cell.get_genome()
        self.assertEqual(genome, self.genome)

    def test_genome_size(self) -> None:
        genome_size = self.cell.get_genome_size()
        self.assertEqual(genome_size, self.genome_size)

    def test_get_traits(self) -> None:
        traits = self.cell.get_traits()
        self.assertEqual(traits, self.traits)

    def test_get_trait_frame(self) -> None:
        traits = self.cell.get_traits()
        for trait in traits:
            trait_frame = self.cell.get_trait_frame(trait=trait)
            self.assertEqual(trait_frame, self.trait2frame[trait])

    def test_get_trait_score(self) -> None:
        traits = self.cell.get_traits()
        for trait in traits:
            trait_score = self.cell.get_trait_score(trait=trait)
            self.assertEqual(trait_score, self.trait2score[trait])

    def test_get_move_step_size(self) -> None:
        move_step_size = self.cell.test_get_move_step_size()
        self.assertEqual(move_step_size, self.move_step_size)

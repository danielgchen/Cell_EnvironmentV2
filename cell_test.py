import unittest
import cell

class CellTests(unittest.TestCase):
    # set up the cell for testing
    def setUp(self) -> None:
        # define ideal sequences
        self.ideal_seqs = {"a": "AAACCCTTTGGG", "b": "AACCTTGG", "c": "ACTG"}
        # define traits
        self.traits = ["a", "b", "c"]
        # define traits to frame
        self.trait2frame = {"a": (0, 10), "b": (10, 20), "c": (20, 30)}
        # define genome
        self.genome = "AAACCCTTTGGGAAACCCTTTGGGAACCTTGGAACCTTGGACTGACTG"
        # define the cell
        self.cell = cell.Cell(
            ideal_seqs=self.ideal_seqs,
            traits=self.traits,
            trait2frame=self.trait2frame,
            genome=self.genome
        )
        # define the expected genome size
        self.genome_size = 48
        # define the expected trait scores
        self.trait2score = {'a': 0.8333333333333334, 'b': 0.25, 'c': 0}

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

    
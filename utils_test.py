import unittest
import utils

class UtilsTests(unittest.TestCase):
    def setUp(self) -> None:
        # inputs for test_gen_rand_genome
        self.genome = "TGGCCAAAAT"

    def test_gen_rand_genome(self) -> None:
        # due to the random nature it is difficult to test
        genome = utils.gen_rand_genome()
        self.assertEqual(genome, self.genome)
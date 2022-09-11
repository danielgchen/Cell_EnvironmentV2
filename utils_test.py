import unittest
import utils
import numpy as np


class UtilsTests(unittest.TestCase):
    def setUp(self) -> None:
        # inputs for test_gen_genome
        self.genome = "TGGCCAAAATGTGGTGGGGTCTGACTGATGTAATAGACCCCAAAAGGGCG"
        # inputs for test_gen_frame
        self.frame = (7, 9)
        # inputs for test_gen_mut_type
        self.mut_type = "sub"
        # inputs for test_gen_mut_sub
        self.mut_sub = "T"
        # inputs for test_gen_mut_ins
        self.mut_ins = "T"
        # inputs for test_gen_mut
        self.mut = "C"
        # inputs for test_gen_mut_frame
        self.mut_frame = 2

    def test_gen_genome(self) -> None:
        rng = np.random.default_rng(0)
        genome = utils.gen_genome(rng=rng)
        self.assertEqual(genome, self.genome)

    def test_gen_frame(self) -> None:
        rng = np.random.default_rng(0)
        frame = utils.gen_frame(size=10, rng=rng)
        self.assertEqual(frame, self.frame)

    def test_gen_mut_type(self) -> None:
        rng = np.random.default_rng(0)
        mut_type = utils.gen_mut_type(0.9, rng=rng)
        self.assertEqual(mut_type, self.mut_type)

    def test_gen_mut_sub(self) -> None:
        rng = np.random.default_rng(0)
        mut_sub = utils.gen_mut_sub("A", rng=rng)
        self.assertEqual(mut_sub, self.mut_sub)

    def test_gen_mut_ins(self) -> None:
        rng = np.random.default_rng(0)
        mut_ins = utils.gen_mut_ins(rng=rng)
        self.assertEqual(mut_ins, self.mut_ins)

    def test_gen_mut(self) -> None:
        rng = np.random.default_rng(0)
        mut = utils.gen_mut(0.9, "A", rng=rng)
        self.assertEqual(mut, self.mut)

    def test_gen_mut_frame(self) -> None:
        rng = np.random.default_rng(0)
        mut_frame = utils.gen_mut_frame(3, 0.9, rng=rng)
        self.assertEqual(mut_frame, self.mut_frame)

import numpy as np
import utils
import constants
from typing import Optional, List
from Levenshtein import distance as levenshtein_distance


# define the cell class
class Cell:
    def __init__(self, traits: Optional[List[str]] = None):
        # genome
        self.genome = utils.gen_genome()
        self.genome_size = len(self.genome)
        # traits
        self.traits = constants.CELL_TRAITS if traits is None else traits
        # traits and frames
        self.trait2frame = {}
        for trait in self.traits:
            self.trait2frame[trait] = utils.gen_frame(size=self.genome_size)
        # traits and scores
        self.trait2score = {trait: np.nan for trait in self.traits}

    # calculation functions
    def calc_trait_score(self, trait: str, ideal_seq: str):
        """
        trait is scored based on levenshtein distance between
        the cell's trait's sequence and the ideal sequence
        as defined from the environment

        @param trait = key to access the cell's sequence
        @param ideal_seq = the ideal sequence for this gene
        @returns score = score from 1 to 0 of the trait
        """
        frame = self.trait2frame[trait]
        self_seq = self.genome[frame[0]:frame[1]]
        dist = levenshtein_distance(self_seq, ideal_seq)
        if (dist > len(ideal_seq)):
            self.trait2score[trait] = 0
        else:
            self.trait2score[trait] = 1 - (dist / len(ideal_seq))

    # get functions
    def get_genome(self) -> str:
        """
        get function for the genome
        """
        return self.genome

    def get_genome_size(self) -> int:
        """
        get function for the genome's size
        """
        return self.genome_size

    def get_traits(self) -> Optional[List[str]]:
        """
        get function for the cell's traits
        """
        return self.traits

    def get_trait_frame(self, trait: str) -> float:
        """
        get function for a the frame of a given trait
        """
        return self.trait2frame[trait]

    def get_trait_score(self, trait: str) -> float:
        """
        get function for a the score of a given trait
        """
        return self.trait2score[trait]
import source.utils as utils
import numpy as np
import source.constants as constants
from typing import Dict, List, Optional, Tuple
from Levenshtein import distance as levenshtein_distance


# define the cell class
class Cell:
    def __init__(
        self,
        ideal_seqs: Dict[str, str],
        traits: List[str],
        trait2frame: Optional[Dict[str, Tuple[int, int]]] = None,
        genome: Optional[str] = None,
    ):
        # genome
        self.genome = utils.gen_genome() if genome is None else genome
        self.genome_size = len(self.genome)
        # traits
        self.traits = traits
        # traits and frames
        self.trait2frame = {}
        for trait in self.traits:
            if trait2frame and trait in trait2frame:
                self.trait2frame[trait] = trait2frame[trait]
            else:
                self.trait2frame[trait] = utils.gen_frame(size=self.genome_size)
        # traits and scores
        self.trait2score = {}
        for trait in self.traits:
            if trait in ideal_seqs:
                self.calc_trait_score(trait=trait, ideal_seq=ideal_seqs[trait])
        # position
        self.position = np.array([0, 0])  # TODO: de-hardcode the position
        # movement
        self.move_step_size = constants.MOVE_STEP_SIZE  # TODO: change this to mutatable
        # energy
        self.energy = constants.INITIAL_ENERGY

    # movement functions
    def move(self):
        """
        movement magnitude is determined by self.move_step_size energy cost
        is determined by step size multiplied by trait score for movement 
        as we consider step size to require a linear higher cost
        """
        # calculate deltas
        deltas = utils.gen_deltas(magnitude=self.move_step_size)
        # calculate new positions
        position_hat = self.position + self.deltas
        # TODO: add canvas based adjustments
        # reassign position to new positions
        self.position = position_hat
        # calculate the energy
        distance = np.linalg.norm(deltas)
        cost_scaler = self.get_trait_score("move")
        energy_cost = distance * (1 - cost_scaler)
        # update the energy
        self.energy -= energy_cost


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
        self_seq = self.genome[frame[0] : frame[1]]
        dist = levenshtein_distance(self_seq, ideal_seq)
        if dist > len(ideal_seq):
            self.trait2score[trait] = 0
        else:
            self.trait2score[trait] = 1 - (dist / len(ideal_seq))

    # mutation functions
    def mut_genome(self) -> str:
        """
        mutates the genome using given mutation threshold
        and loops through the entire genome

        @returns mut_genome = mutated genome
        """
        mut_genome = ""
        for idx in range(len(self.genome)):
            curr_nuc = self.genome[idx]
            nuc = utils.gen_mut(threshold=self.trait2score["mutate"], curr_nuc=curr_nuc)
            mut_genome += nuc
        return mut_genome

    def mut_frame(self, trait: str) -> Tuple[int]:
        """
        mutates the reading frame for a given trait

        @returns mut_frame = mutate frame
        """
        start = utils.gen_mut_frame(
            value=self.trait2frame[trait][0], threshold=self.trait2score["mutate"]
        )
        end = utils.gen_mut_frame(
            value=self.trait2frame[trait][1], threshold=self.trait2score["mutate"]
        )
        mut_frame = (min(start, end), max(start, end))
        return mut_frame

    def mut_self(self) -> Dict:
        """
        mutates all attributes

        @returns kwargs = can be used to create a new cell
        """
        mut_genome = self.mut_genome()
        mut_trait2frame = {}
        for trait in self.traits:
            mut_trait2frame[trait] = self.mut_frame(trait=trait)
        kwargs = {"genome": mut_genome, "trait2frame": mut_trait2frame}
        return kwargs

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
        get function for the frame of a given trait
        """
        return self.trait2frame[trait]

    def get_trait_score(self, trait: str) -> float:
        """
        get function for the score of a given trait
        """
        return self.trait2score[trait]

    def get_move_step_size(self) -> float:
        """
        get function for the step size of a movement
        """
        return self.move_step_size

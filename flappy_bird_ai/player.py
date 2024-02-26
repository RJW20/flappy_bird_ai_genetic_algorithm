from copy import deepcopy

import numpy as np

from flappy_bird_app import Bird
from genetic_algorithm import BasePlayer


class Player(Bird, BasePlayer):
    """Bird with a Genome to control its movements."""

    def __init__(self) -> None:
        self.score: int = 0
        self.fitness: int = 0
        self.best_score: int = 0
        self.vision: np.ndarray

    def look(self) -> None:
        """Set the bird's vision.
        
        Can see: distance to the pipe, own vertical velocity, vertical distance 
        to the end of the top of the pipe, vertical distance to the end of the 
        bottom of the pipe.
        """

        first_pipe = self.pipes.items[0]
        self.vision = np.array[first_pipe.position - self.x, 
                               self.velocity,
                               self.position - first_pipe.height, 
                               first_pipe.bottom_height - self.position]

    def think(self) -> int:
        """Feed the input into the Genome and turn the output into a valid move."""
        
        genome_output = self.genome.propagate(self.vision)
        return round(genome_output[0], 1)      #jump if > 0.5 (sigmoid activation)

    def empty_clone(self) -> BasePlayer:
        """Return a new instance of self's class without a genome."""

        clone = deepcopy(self)
        clone.fitness = 0
        clone.best_score = 0
        clone.genome = None

        return clone
from copy import deepcopy

import numpy as np

from flappy_bird_app import Bird
from genetic_algorithm import BasePlayer


class Player(Bird, BasePlayer):
    """Bird with a Genome to control its movements."""

    def __init__(self) -> None:
        super(Player, self).__init__()
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
        self.vision = np.array([first_pipe.position - self.x, 
                               self.velocity,
                               self.position - first_pipe.height, 
                               first_pipe.bottom_height - self.position])

    def think(self) -> int:
        """Feed the vision into the Genome and turn the output into a valid move."""
        
        genome_output = self.genome.propagate(self.vision)
        return round(genome_output[0])      #move takes 0 or 1, genome_output~[0,1]
    
    def __getstate__(self) -> dict:
        """Return a dictionary containing attribute names and their values as (key, value) pairs.
        
        All values must also be pickleable i.e. not use __slots__ or have __getstate__ and __setstate__ methods like this.
        If this class uses __slots__ or extends one that does this must be changed.
        """

        return self.__dict__

    def __setstate__(self, d: dict) -> BasePlayer:
        """Load the attributes in the dictionary d into self.
        
        If this class uses __slots__ or extends one that does this must be changed.
        """

        self.__dict__ = d

    def empty_clone(self) -> BasePlayer:
        """Return a new instance of self's class without a genome."""

        clone = deepcopy(self)
        clone.fitness = 0
        clone.best_score = 0
        clone.genome = None

        return clone
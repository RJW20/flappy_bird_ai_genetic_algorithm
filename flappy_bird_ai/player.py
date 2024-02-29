from copy import deepcopy

import numpy as np

from flappy_bird_app import Bird
from genetic_algorithm import BasePlayer
from flappy_bird_app.bird import MAX_VELOCITY


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

        front_pipe = self.pipes.items[0]
        if self.x - self.radius > front_pipe.position + front_pipe.width:
            front_pipe = self.pipes.items[1]
        self.vision = np.array([max((front_pipe.position - self.x)/(1 - self.x), 0), 
                               self.velocity/MAX_VELOCITY,
                               max(self.position - front_pipe.height,0), 
                               max(front_pipe.bottom_height - self.position,0)])

    def think(self) -> int:
        """Feed the vision into the Genome and turn the output into a valid move."""
        
        genome_output = self.genome.propagate(self.vision)
        return round(genome_output[0])      #move takes 0 or 1, genome_output~[0,1]

    def empty_clone(self) -> BasePlayer:
        """Return a new instance of self's class without a genome."""

        clone = deepcopy(self)
        clone.fitness = 0
        clone.best_score = 0
        clone.genome = None

        return clone
import numpy as np

from flappy_bird_app import Bird
from genetic_algorithm import BasePlayer


class Player(Bird, BasePlayer):
    """Bird with a Genome to control its movements."""

    def __init__(self) -> None:
        self.score: int = 0
        self.fitness: int = 0
        self.best_score: int = 0

    def look(self) -> None:
        """Update the attributes used as input to the Genome."""
        pass

    def think(self) -> int:
        """Feed the input into the Genome and turn the output into a valid move."""
        pass 

    def empty_clone(self) -> BasePlayer:
        """Return a new instance of self's class without a genome."""
        pass
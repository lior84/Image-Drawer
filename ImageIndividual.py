from typing import List
from eckity.fitness.fitness import Fitness
from eckity.individual import Individual

class ImageIndividual(Individual):
    def __init__(self, image_array: List[List[tuple]], dist, fitness: Fitness):
        super().__init__(fitness)
        self.image_array = image_array
        self.dist = dist

    def show(self):
        pass
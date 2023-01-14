import random
from eckity.fitness.simple_fitness import SimpleFitness
from eckity.genetic_operators.genetic_operator import GeneticOperator
from ImageIndividual import ImageIndividual

class ImageCrossover(GeneticOperator):
    def __init__(self, population_size , probability=1, arity=2, events=None):
        super().__init__(probability, arity, events)
        self.population_size = population_size

    def apply(self, individuals):
        return self.create_child(individuals[0], individuals[1])

    def create_child(self, individual_parent1, individual_parent2):
        image_array = []
        height = len(individual_parent1.image_array)
        width = len(individual_parent1.image_array[0])
        avg_dist = 0
        for i in range(height):
            row = []
            for j in range(width):
                coin_toss = random.random()
                if coin_toss < 0.5:
                    element = individual_parent1.image_array[i][j]
                else:
                    element = individual_parent2.image_array[i][j]
                avg_dist += element.dist
                row.append(element)
            image_array.append(row)
        avg_dist /= (height * width)

        return ImageIndividual(image_array, avg_dist, SimpleFitness(higher_is_better=False))
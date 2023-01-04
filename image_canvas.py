import random
from typing import List

from eckity.algorithms.simple_evolution import SimpleEvolution
from eckity.creators.creator import Creator
from eckity.evaluators.simple_individual_evaluator import SimpleIndividualEvaluator
from eckity.fitness.fitness import Fitness
from eckity.fitness.simple_fitness import SimpleFitness
from eckity.genetic_operators.genetic_operator import GeneticOperator
from eckity.genetic_operators.selections.tournament_selection import TournamentSelection
from eckity.individual import Individual
from tkinter import *
import numpy as np
from eckity.statistics.best_average_worst_statistics import BestAverageWorstStatistics
from eckity.subpopulation import Subpopulation
from numpy import sqrt
from PIL import Image

from Pixel import Pixel



class ImageIndividual(Individual):
    def __init__(self, image_array: List[List[tuple]], fitness: Fitness):
        super().__init__(fitness)
        self.image_array = image_array

    def show(self):
        pass


class ImageCreator(Creator):
    def __init__(self):
        super().__init__()
        self.target = self.get_target_image_array("mona_lisa.png")
        self.height = len(self.target)
        self.width = len(self.target[0])

    def get_target_image_array(self, path):
        img = Image.open(path)
        img.load()

        pixel_values = list(img.getdata())
        return self.convert_to_touple(np.array(pixel_values).reshape((img.height, img.width, 3)))

    def convert_to_touple(self, array3d):
        new_arr = []
        for outer_arr in array3d:
            # Create a new sublist to hold the tuple elements
            inner_arr = []
            # Iterate over the outer array
            for inner in outer_arr:
                # Convert the inner array to a tuple and append it to the inner sublist
                inner_arr.append(tuple(inner))
            # Append the inner sublist to the new array
            new_arr.append(inner_arr)
        return new_arr

    def create_individuals(self, n_individuals, higher_is_better):
        return [ImageIndividual(self.random_image_array(), SimpleFitness(higher_is_better=higher_is_better)) for _ in
                range(n_individuals)]

    def random_image_array(self):
        return self.create_random_array()


    def create_random_array(self):
        pixel_array = [[0 for _ in range(self.width)] for _ in range(self.height)]
        for i, row in enumerate(pixel_array):
            for j, element in enumerate(row):
                pixel_array[i][j] = self.get_random_pixel(i, j)

        return pixel_array

    def get_pixel_distance(self, p1, p2):
        return sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2 + (p1[2] - p2[2]) ** 2)

    def get_random_pixel(self, i, j):
        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)

        curr_pixel = (r, g, b)
        target_corresponding_pixel = self.target[i][j]

        pixel_dist = self.get_pixel_distance(curr_pixel, target_corresponding_pixel)
        return Pixel(curr_pixel, pixel_dist)

class ImageEvaluator(SimpleIndividualEvaluator):
    def __init__(self):
        super().__init__()

    def _evaluate_individual(self, individual: ImageIndividual):
        dist = 0
        for i, row in enumerate(individual.image_array):
            for j, element in enumerate(row):
                dist += element.dist
        dist /= (len(individual.image_array) * (len(individual.image_array[0])))
        return dist

class ImageCrossover(GeneticOperator):
    def __init__(self, probability=1, arity=2, events=None):
        super().__init__(probability, arity, events)

    def apply(self, individuals):
        children = []

        for i in range(len(individuals) - 1):
            individual1 = individuals[i]
            individual2 = individuals[i + 1]
            children.append(self.create_child(individual1, individual2))

        return children

    def create_child(self, individual_parent1, individual_parent2):
        image_array = []
        height = len(individual_parent1.image_array)
        width = len(individual_parent1.image_array[0])

        for i in range(height):
            row = []
            for j in range(width):
                coin_toss = random.random()
                if coin_toss < 0.5:
                    element = individual_parent1.image_array[i][j]
                else:
                    element = individual_parent2.image_array[i][j]

                row.append(element)
            image_array.append(row)

        return ImageIndividual(image_array, SimpleFitness(higher_is_better=False))

class ImageStatistics(BestAverageWorstStatistics):
    def __init__(self):
        super().__init__()

    def write_statistics(self, sender, data_dict):
        super().write_statistics(sender, data_dict)
        best_individual = data_dict["population"].sub_populations[0].get_best_individual()
        generation = data_dict["generation_num"]


def evolution_algo(population_size=30, n_generations=50, elitism_rate=0.01, individuals=None):
    return SimpleEvolution(
        population=Subpopulation(
            evaluator=ImageEvaluator(),
            creators=ImageCreator(),
            pcr=None,
            operators_sequence=[
                ImageCrossover()
            ],
            selection_methods=[
                (TournamentSelection(tournament_size=2, higher_is_better=True, events=None), 1)
            ],
            elitism_rate=elitism_rate,
            population_size=population_size,
            individuals=individuals,
            higher_is_better=True
        ),
        max_generation=n_generations,
        max_workers=None,  # uses all available cores
        statistics=ImageStatistics(),
    )

evolution_algo().evolve()

exit()

creator = ImageCreator()
population = creator.create_individuals(10, False)

evaluator = ImageEvaluator()
score = evaluator._evaluate_individual(population[0])

crossover = ImageCrossover()


next_gen = crossover.apply(population)
score_2 = evaluator._evaluate_individual(next_gen[0])


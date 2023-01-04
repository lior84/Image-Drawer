from random import random
from typing import List
from eckity.algorithms.simple_evolution import SimpleEvolution
from eckity.breeders.simple_breeder import SimpleBreeder
from eckity.creators.creator import Creator
from eckity.creators.ga_creators.bit_string_vector_creator import GABitStringVectorCreator
from eckity.evaluators.simple_individual_evaluator import SimpleIndividualEvaluator
from eckity.fitness.fitness import Fitness
from eckity.genetic_operators.crossovers.vector_k_point_crossover import VectorKPointsCrossover
from eckity.genetic_operators.mutations.vector_random_mutation import BitStringVectorNFlipMutation
from eckity.genetic_operators.selections.tournament_selection import TournamentSelection
from eckity.individual import Individual
from eckity.statistics.best_average_worst_statistics import BestAverageWorstStatistics
from eckity.subpopulation import Subpopulation
from eckity.termination_checkers.threshold_from_target_termination_checker import ThresholdFromTargetTerminationChecker
from tkinter import *
import numpy as np
from numpy import sqrt
from PIL import Image

class ImageCanvas:
    def __init__(self, image_array: List[List[tuple]]):
        self.image_array = image_array


class ImageIndividual(Individual):
    def __init__(self, image_canvas: ImageCanvas, fitness: Fitness):
        super().__init__(fitness)
        self.image_canvas = image_canvas

    def show(self):
        pass


class ImageCreator(Creator):
    def __init__(self):
        super().__init__()
        self.target = self.get_target_image_array("mona_lisa.png")

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
        return [ImageIndividual(self.random_strategy(), SimpleFitness(higher_is_better=higher_is_better)) for _ in
                range(n_individuals)]

    def random_strategy(self):
        image_array = [[self.random_action() for _ in range(Strategy.hard_hands_dim[1])] for _ in
                      range(Strategy.hard_hands_dim[0])]

        return Strategy(hard_hands=hard_hands, soft_hands=soft_hands)

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

    @staticmethod
    def random_action():
        return random.choice(list(Action))

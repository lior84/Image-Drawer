import random
from math import sqrt
import numpy as np
from PIL import Image
from eckity.creators.creator import Creator
from eckity.fitness.simple_fitness import SimpleFitness
from ImageIndividual import ImageIndividual
from Pixel import Pixel

class ImageCreator(Creator):
    def __init__(self):
        super().__init__()
        self.target = self.get_target_image_array("mona_lisa.png")
        self.height = len(self.target)
        self.width = len(self.target[0])

    def get_target_image_array(self, path):
        img = Image.open(path)

        self.width = 30
        self.height = 45
        img = img.resize((self.width, self.height), Image.ANTIALIAS)

        img.load()

        pixel_values = list(img.getdata())
        return self.convert_to_touple(np.array(pixel_values).reshape((img.height, img.width, 3)))

    def convert_to_touple(self, array3d):
        new_arr = []
        for outer_arr in array3d:
            inner_arr = []
            for inner in outer_arr:
                inner_arr.append(tuple(inner))
            new_arr.append(inner_arr)
        return new_arr

    def create_individuals(self, n_individuals, higher_is_better):
        individuals = []
        for _ in range(n_individuals):
            random_array, dist = self.random_image_array()
            individuals.append(ImageIndividual(random_array, dist,  SimpleFitness(higher_is_better=higher_is_better)))

        return individuals

    def random_image_array(self):
        return self.create_random_array()

    def create_random_array(self):
        avg_dist = 0
        pixel_array = [[0 for _ in range(self.width)] for _ in range(self.height)]
        for i, row in enumerate(pixel_array):
            for j, element in enumerate(row):
                pixel_array[i][j] = self.get_random_pixel(i, j)
                avg_dist += pixel_array[i][j].dist
        avg_dist /= (self.height * self.width)
        return pixel_array, avg_dist

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

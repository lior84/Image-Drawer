from PIL import ImageDraw, Image
from eckity.statistics.best_average_worst_statistics import BestAverageWorstStatistics

class ImageStatistics(BestAverageWorstStatistics):
    def __init__(self):
        super().__init__()

    def write_statistics(self, sender, data_dict):
        super().write_statistics(sender, data_dict)
        best_individual = data_dict["population"].sub_populations[0].get_best_individual()
        generation = data_dict["generation_num"]

        if generation % 25 == 0:
            self.print_image(best_individual)

    def print_image(self, best_individual):
        pixel_array = best_individual.image_array
        img = Image.new("RGB", (len(pixel_array[0]), len(pixel_array)))
        drawer = ImageDraw.Draw(img)

        for y, row in enumerate(pixel_array):
            for x, pixel in enumerate(row):
                drawer.point((x, y), fill=pixel.rgb)

        width = 400
        height = 600
        img = img.resize((width, height), Image.ANTIALIAS)

        img.show()
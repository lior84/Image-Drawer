from eckity.evaluators.simple_individual_evaluator import SimpleIndividualEvaluator
import ImageIndividual

class ImageEvaluator(SimpleIndividualEvaluator):
    def __init__(self):
        super().__init__()

    def _evaluate_individual(self, individual: ImageIndividual):
        return individual.dist
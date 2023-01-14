from eckity.algorithms.simple_evolution import SimpleEvolution
from eckity.subpopulation import Subpopulation
from eckity.termination_checkers.threshold_from_target_termination_checker import ThresholdFromTargetTerminationChecker
from ImageBreeder import ImageBreeder
from ImageCreator import ImageCreator
from ImageCrossover import ImageCrossover
from ImageEvaluator import ImageEvaluator
from ImageStatistics import ImageStatistics
from TournamentImageSelection import TournamentImageSelection

def evolution_algo(population_size=2000, n_generations=10000, elitism_rate=0.01, individuals=None):
    return SimpleEvolution(
        population=Subpopulation(
            evaluator=ImageEvaluator(),
            creators=ImageCreator(),
            pcr=None,
            operators_sequence=[
                ImageCrossover(population_size)
            ],
            selection_methods=[
                (TournamentImageSelection(tournament_size=60, higher_is_better=False, events=None), 20)
            ],
            elitism_rate=elitism_rate,
            population_size=population_size,
            individuals=individuals,
            higher_is_better=False,
        ),
        max_generation=n_generations,
        max_workers=None,
        statistics=ImageStatistics(),
        breeder=ImageBreeder(),
        termination_checker=ThresholdFromTargetTerminationChecker(optimal=0, threshold=45)
    )

evolution_algo().evolve()

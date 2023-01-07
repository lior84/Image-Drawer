import random

from eckity.breeders.breeder import Breeder
from eckity.genetic_operators.selections.elitism_selection import ElitismSelection


class ImageBreeder(Breeder):
    def __init__(self,
                 events=None):
        super().__init__(events=events)
        self.selected_individuals = []
        self.best_of_run = []

    def apply_breed(self, population):

        for subpopulation in population.sub_populations:
            nextgen_population = []

            num_elites = subpopulation.n_elite
            if num_elites > 0:
                elitism_sel = ElitismSelection(num_elites=num_elites, higher_is_better=subpopulation.higher_is_better)
                elitism_sel.apply_operator((subpopulation.individuals, nextgen_population))

            self.selected_individuals = subpopulation.get_selection_methods()[0][0] \
                .select(subpopulation.individuals, nextgen_population)

            # then runs all operators on next_gen
            nextgen_population = self._apply_operators(subpopulation.get_operators_sequence(),
                                                       self.selected_individuals)

            subpopulation.individuals = nextgen_population

    def _apply_operators(self, operator_seq, individuals_to_apply_on):
        new_gen = []

        for operator in operator_seq:
            operator_arity = operator.get_operator_arity()

            while len(new_gen) < len(individuals_to_apply_on):
                parent1 = random.choice(individuals_to_apply_on)
                parent2 = random.choice(individuals_to_apply_on)

                op_res = operator.apply_operator([parent1, parent2])
                new_gen.append(op_res)
        print("len: ", len(new_gen))
        return new_gen

    def event_name_to_data(self, event_name):
        if event_name == "after_selection":
            return {"selected_individuals": self.selected_individuals,
                    "best_of_run": self.best_of_run}

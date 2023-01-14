import random
from eckity.genetic_operators.selections.selection_method import SelectionMethod

class TournamentImageSelection(SelectionMethod):
    def __init__(self, tournament_size, higher_is_better=False, events=None):
        super().__init__(events=events, higher_is_better=higher_is_better)
        self.tournament_size = tournament_size

    def select(self, source_inds, dest_inds):
        n_tournaments = (len(source_inds) - len(dest_inds))

        winners = []
        for _ in range(n_tournaments):
            tour = random.choices(source_inds, k=self.tournament_size)
            winner = self._pick_tournament_winner(tour)
            if(winners.count(winner) == 2):
                source_inds.remove(winner)
            winners.append(winner)

        dest_inds.extend(winners)

        self.selected_individuals = dest_inds

        return dest_inds

    def _pick_tournament_winner(self, tournament):
        winner = tournament[0]
        for participant in tournament[1:]:
            if participant.fitness.better_than(participant, winner.fitness, winner):
                winner = participant
        return winner
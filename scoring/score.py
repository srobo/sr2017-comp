
class Scorer:
    def __init__(self, teams_data, arena_data = None):
        self._teams_data = teams_data,
        self._arena_data = arena_data or {}

    def calculate_scores(self):
        scores = {tla: 0 for tla in self._scoresheet.keys()}
        return scores

    def validate(self, extra):
        pass

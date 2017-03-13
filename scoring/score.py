
from collections import Counter

class InvalidScoresheetException(Exception):
    pass

class Scorer:
    EXPECTED_TOKEN_COUNTS = {
        'A': 4,
        'B': 4,
        'C': 1,
    }

    def __init__(self, teams_data, arena_data):
        self._teams_data = teams_data
        self._arena_data = arena_data

    def calculate_scores(self):
        scores = {}
        for tla, info in self._teams_data.items():
            zone = info['zone']
            tokens = self._arena_data[zone]['tokens']

            # 1 point per token
            points = len(tokens)

            counts = Counter(tokens)

            if 'A' in counts and 'B' in counts:
                # 1 further point per B token if there's an A token
                points += counts['B']

                # 2 further points per C token if there are both A and B tokens
                points += 2 * counts.get('C', 0)

            scores[tla] = points

        return scores

    def validate(self, extra):
        all_tokens = ''.join(
            d['tokens']
            for d in self._arena_data.values()
        ).replace(' ', '')

        counts = Counter(all_tokens)

        if counts != self.EXPECTED_TOKEN_COUNTS:
            msg = "Found invalid token counts {0!r} (expecting: {1!r})".format(
                dict(counts),
                self.EXPECTED_TOKEN_COUNTS,
            )
            raise InvalidScoresheetException(msg)


if __name__ == '__main__':
    import libproton
    libproton.main(Scorer)

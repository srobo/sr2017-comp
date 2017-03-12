
from collections import Counter

class InvalidScoresheetException(Exception):
    pass

class Scorer:
    VALID_TOKENS = 'ABC'

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

        num_tokens = len(all_tokens)
        if not num_tokens == 9:
            msg = "Should have exactly 9 tokens (got {0})".format(num_tokens)
            raise InvalidScoresheetException(msg)

        valid_tokens = set(self.VALID_TOKENS)
        actual_tokens = set(all_tokens)
        extras = actual_tokens - valid_tokens
        if extras:
            extras_str = ', '.join(extras)
            valid_str =  ', '.join(valid_tokens)
            msg = "Found invalid tokens {0} (valid: {1})".format(extras_str, valid_str)
            raise InvalidScoresheetException(msg)


if __name__ == '__main__':
    import libproton
    libproton.main(Scorer)

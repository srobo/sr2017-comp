
from score import Scorer

# Path hackery
import os.path
import sys
ROOT = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.insert(0, ROOT)

from score import Scorer, InvalidScoresheetException

def test_scores_match_start():
    teams_data = {
        'ABC': {'zone': 0},
        'DEF': {'zone': 1},
        'GHI': {'zone': 2},
    }
    arena_data = {
        0: { 'tokens': '' },
        1: { 'tokens': '' },
        2: { 'tokens': '' },
        3: { 'tokens': '' },
        'other': { 'tokens': 'AAAA BBBB C' },
    }
    expected = {
        'ABC': 0,
        'DEF': 0,
        'GHI': 0,
    }

    scorer = Scorer(teams_data, arena_data)
    scores = scorer.calculate_scores()

    assert expected == scores, "Wrong scores!"

def test_scores_one_zone_1():
    teams_data = {
        'ABC': {'zone': 0},
        'DEF': {'zone': 1},
        'GHI': {'zone': 2},
    }
    arena_data = {
        0: { 'tokens': '' },
        1: { 'tokens': '' },
        2: { 'tokens': 'ABA' },
        3: { 'tokens': '' },
        'other': { 'tokens': 'AA BBB C' },
    }
    expected = {
        'ABC': 0,
        'DEF': 0,
        'GHI': 4,
    }

    scorer = Scorer(teams_data, arena_data)
    scores = scorer.calculate_scores()

    assert expected == scores, "Wrong scores!"

def test_scores_one_zone_2():
    teams_data = {
        'ABC': {'zone': 0},
        'DEF': {'zone': 1},
        'GHI': {'zone': 2}
    }
    arena_data = {
        0: { 'tokens': '' },
        1: { 'tokens': 'AC' },
        2: { 'tokens': '' },
        3: { 'tokens': '' },
        'other': { 'tokens': 'AAA BBBB C' },
    }
    expected = {
        'ABC': 0,
        'DEF': 2,
        'GHI': 0,
    }

    scorer = Scorer(teams_data, arena_data)
    scores = scorer.calculate_scores()

    assert expected == scores, "Wrong scores!"

def test_scores_combined():
    teams_data = {
        'ABC': {'zone': 0},
        'DEF': {'zone': 1},
        'GHI': {'zone': 2}
    }
    arena_data = {
        0: { 'tokens': '' },
        1: { 'tokens': 'AC' },
        2: { 'tokens': 'AAB' },
        3: { 'tokens': '' },
        'other': { 'tokens': 'A BBB' },
    }
    expected = {
        'ABC': 0,
        'DEF': 2,
        'GHI': 4,
    }

    scorer = Scorer(teams_data, arena_data)
    scores = scorer.calculate_scores()

    assert expected == scores, "Wrong scores!"

def test_scores_no_A():
    teams_data = {
        'ABC': {'zone': 0},
        'DEF': {'zone': 1},
        'GHI': {'zone': 2}
    }
    arena_data = {
        0: { 'tokens': '' },
        1: { 'tokens': 'BBC' },
        2: { 'tokens': '' },
        3: { 'tokens': '' },
        'other': { 'tokens': 'AAAA BB' },
    }
    expected = {
        'ABC': 0,
        'DEF': 3,
        'GHI': 0,
    }

    scorer = Scorer(teams_data, arena_data)
    scores = scorer.calculate_scores()

    assert expected == scores, "Wrong scores!"

def test_scores_AC_no_B():
    teams_data = {
        'ABC': {'zone': 0},
        'DEF': {'zone': 1},
        'GHI': {'zone': 2}
    }
    arena_data = {
        0: { 'tokens': '' },
        1: { 'tokens': 'AC' },
        2: { 'tokens': '' },
        3: { 'tokens': '' },
        'other': { 'tokens': 'AAA BBBB' },
    }
    expected = {
        'ABC': 0,
        'DEF': 2,
        'GHI': 0,
    }

    scorer = Scorer(teams_data, arena_data)
    scores = scorer.calculate_scores()

    assert expected == scores, "Wrong scores!"

def test_validate_error_invalid_notation():
    teams_data = {
        'ABC': {'zone': 0},
        'DEF': {'zone': 1},
        'GHI': {'zone': 2},
    }
    arena_data = {
        0: { 'tokens': '' },
        1: { 'tokens': 'A' },
        2: { 'tokens': '' },
        3: { 'tokens': '' },
        'other': { 'tokens': 'W' * 8 },
    }

    try:
        scorer = Scorer(teams_data, arena_data)
        scores = scorer.validate(None)
    except InvalidScoresheetException:
        pass
    else:
        assert False, "Should error when there are invalid tokens"

def test_validate_error_too_many_A_tokens():
    teams_data = {
        'ABC': {'zone': 0},
        'DEF': {'zone': 1},
        'GHI': {'zone': 2},
    }
    arena_data = {
        0: { 'tokens': '' },
        1: { 'tokens': 'AA BB C' },
        2: { 'tokens': '' },
        3: { 'tokens': '' },
        'other': { 'tokens': 'AAA BB' },
    }

    try:
        scorer = Scorer(teams_data, arena_data)
        scores = scorer.validate(None)
    except InvalidScoresheetException:
        pass
    else:
        assert False, "Should error when there are too many A tokens"

def test_validate_error_too_many_B_tokens():
    teams_data = {
        'ABC': {'zone': 0},
        'DEF': {'zone': 1},
        'GHI': {'zone': 2},
    }
    arena_data = {
        0: { 'tokens': '' },
        1: { 'tokens': 'AA BB C' },
        2: { 'tokens': '' },
        3: { 'tokens': '' },
        'other': { 'tokens': 'AA BBB' },
    }

    try:
        scorer = Scorer(teams_data, arena_data)
        scores = scorer.validate(None)
    except InvalidScoresheetException:
        pass
    else:
        assert False, "Should error when there are too many B tokens"

def test_validate_error_too_many_C_tokens():
    teams_data = {
        'ABC': {'zone': 0},
        'DEF': {'zone': 1},
        'GHI': {'zone': 2},
    }
    arena_data = {
        0: { 'tokens': '' },
        1: { 'tokens': 'AA BB C' },
        2: { 'tokens': '' },
        3: { 'tokens': '' },
        'other': { 'tokens': 'AA BB C' },
    }

    try:
        scorer = Scorer(teams_data, arena_data)
        scores = scorer.validate(None)
    except InvalidScoresheetException:
        pass
    else:
        assert False, "Should error when there are too many C tokens"

def test_validate_error_too_few_A_tokens():
    teams_data = {
        'ABC': {'zone': 0},
        'DEF': {'zone': 1},
        'GHI': {'zone': 2},
    }
    arena_data = {
        0: { 'tokens': '' },
        1: { 'tokens': 'A BB C' },
        2: { 'tokens': '' },
        3: { 'tokens': '' },
        'other': { 'tokens': 'AA BB' },
    }

    try:
        scorer = Scorer(teams_data, arena_data)
        scores = scorer.validate(None)
    except InvalidScoresheetException:
        pass
    else:
        assert False, "Should error when there are too few A tokens"

def test_validate_error_too_few_B_tokens():
    teams_data = {
        'ABC': {'zone': 0},
        'DEF': {'zone': 1},
        'GHI': {'zone': 2},
    }
    arena_data = {
        0: { 'tokens': '' },
        1: { 'tokens': 'AA BB C' },
        2: { 'tokens': '' },
        3: { 'tokens': '' },
        'other': { 'tokens': 'AA B' },
    }

    try:
        scorer = Scorer(teams_data, arena_data)
        scores = scorer.validate(None)
    except InvalidScoresheetException:
        pass
    else:
        assert False, "Should error when there are too few B tokens"

def test_validate_error_too_few_C_tokens():
    teams_data = {
        'ABC': {'zone': 0},
        'DEF': {'zone': 1},
        'GHI': {'zone': 2},
    }
    arena_data = {
        0: { 'tokens': '' },
        1: { 'tokens': 'AA BB' },
        2: { 'tokens': '' },
        3: { 'tokens': '' },
        'other': { 'tokens': 'AA BB' },
    }

    try:
        scorer = Scorer(teams_data, arena_data)
        scores = scorer.validate(None)
    except InvalidScoresheetException:
        pass
    else:
        assert False, "Should error when there are too few C tokens"

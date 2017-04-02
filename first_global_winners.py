#!/usr/bin/env python

from __future__ import print_function

from sr.comp.comp import SRComp
from sr.comp.match_period import MatchType
from sr.comp.scores import KnockoutScores
from sr.comp import ranker # pylint: disable=no-name-in-module

NON_UK_TEAMS = (
    'MAI',
    'LFG',
    'TLC',
)

def is_UK_team(tla):
    return tla not in NON_UK_TEAMS


def combined_semis_ranked_poitions(scores, final_match_info):
    semi_1_key = (final_match_info.arena, final_match_info.num - 1)
    semi_2_key = (final_match_info.arena, final_match_info.num - 2)
    semis_keys = (semi_1_key, semi_2_key)

    semis_game_points = {}
    for key in semis_keys:
        semis_game_points.update(
            scores.knockout.game_points[key],
        )

    semis_dsq = [
        tla
        for key in semis_keys
        for tla, pts in scores.knockout.ranked_points[key].items()
        if pts == 0
    ]

    positions = ranker.calc_positions(semis_game_points, semis_dsq)
    ranked_points = ranker.calc_ranked_points(positions, semis_dsq)

    return ranked_points


def compute_awards(scores, final_match_info, teams):
    """
    Determine the top three UK based teams.

    The logic here is that we use the results from the:
    - tiebreaker (if present), with ties resolved by league points
    - finals, with ties resolved by league points
    - semis, treating both semis as a single match; this means that we decide
             by game points across both semis and then resolve ties there by
             league position.
    """
    last_match_key = (final_match_info.arena, final_match_info.num)

    all_resolved_positions = []

    try:
        all_resolved_positions.append(
            scores.knockout.resolved_positions[last_match_key],
        )
        if final_match_info.type == MatchType.tiebreaker:
            all_resolved_positions.insert(
                0,
                scores.tiebreaker.resolved_positions[last_match_key],
            )
    except KeyError:
        # We haven't scored the last match yet
        return "Finals not yet scored"

    semis_positions = combined_semis_ranked_poitions(scores, final_match_info)
    ranked_semis = KnockoutScores.calculate_ranking(
        semis_positions,
        scores.league.positions
    )

    all_resolved_positions.append(ranked_semis)

    top_three = set()
    for tla_positions in all_resolved_positions:
        for tla in tla_positions.keys():
            if is_UK_team(tla):
                top_three.add(tla)
                if len(top_three) == 3:
                    return top_three

    raise AssertionError("Not enough teams!")


if __name__ == '__main__':
    comp = SRComp('.')
    print(compute_awards(
        comp.scores,
        comp.schedule.final_match,
        comp.teams,
    ))

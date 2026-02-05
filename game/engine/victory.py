from game.caravan.caravan import Caravan
from game.caravan.enums import CaravanId, RouteId
from game.engine.exceptions import InvalidOutcome
from game.player.enums import PlayerId
from game.rules.constants import CARAVAN_MAX_SCORE, CARAVAN_MIN_SCORE
from game.state.enums import WinReason
from game.state.game_state import GameState, GameResult


def _score_is_in_victory_range(score: int) -> bool:
	return CARAVAN_MIN_SCORE <= score <= CARAVAN_MAX_SCORE


def _route_winner_between(
		caravan_id_a: CaravanId, caravan_a: Caravan,
		caravan_id_b: CaravanId, caravan_b: Caravan,
) -> CaravanId | None:
	score_a = caravan_a.score
	score_b = caravan_b.score

	score_a_valid = _score_is_in_victory_range(score_a)
	score_b_valid = _score_is_in_victory_range(score_b)

	if not score_a_valid and not score_b_valid:
		return None

	if score_a_valid and not score_b_valid:
		return caravan_id_a
	if score_b_valid and not score_a_valid:
		return caravan_id_b

	if score_a > score_b:
		return caravan_id_a
	if score_b > score_a:
		return caravan_id_b

	return None


def _get_route_winner(state: GameState, route_id: RouteId) -> CaravanId | None:
	caravan_p1_tuple = state.get_caravan_by_route_player(PlayerId.P1, route_id)
	caravan_p2_tuple = state.get_caravan_by_route_player(PlayerId.P2, route_id)

	if caravan_p1_tuple is None or caravan_p2_tuple is None:
		return None

	(caravan_p1_id, caravan_p1) = caravan_p1_tuple
	(caravan_p2_id, caravan_p2) = caravan_p2_tuple

	return _route_winner_between(caravan_p1_id, caravan_p1, caravan_p2_id, caravan_p2)


def _get_route_winner_caravans(state: GameState) -> set[CaravanId]:
	winners = set()

	for route in RouteId:
		winner = _get_route_winner(state, route)

		if winner is not None:
			winners.add(winner)

	return winners


def _all_routes_closed(state: GameState) -> bool:
	for route_id in RouteId:
		caravan_p1_tuple = state.get_caravan_by_route_player(PlayerId.P1, route_id)
		caravan_p2_tuple = state.get_caravan_by_route_player(PlayerId.P2, route_id)

		if caravan_p1_tuple is None or caravan_p2_tuple is None:
			return False

		(_, caravan_p1) = caravan_p1_tuple
		(_, caravan_p2) = caravan_p2_tuple

		if not (_score_is_in_victory_range(caravan_p1.score) or _score_is_in_victory_range(caravan_p2.score)):
			return False

	return True


def _get_caravan_sales_winner(state: GameState) -> GameResult | None:
	winners = _get_route_winner_caravans(state)

	p1_wins = 0
	p2_wins = 0

	for caravan_id in winners:
		if caravan_id.owner == PlayerId.P1:
			p1_wins += 1
		elif caravan_id.owner == PlayerId.P2:
			p2_wins += 1

	p1_has_won = p1_wins >= 2
	p2_has_won = p2_wins >= 2

	if not p1_has_won and not p2_has_won:
		return None

	if p1_has_won and not p2_has_won:
		return GameResult(winner_id=PlayerId.P1,
						  reason=WinReason.TWO_CARAVANS if p1_wins == 2 else WinReason.THREE_CARAVANS,
						  end_turn_number=state.turn_number)

	if p2_has_won and not p1_has_won:
		return GameResult(winner_id=PlayerId.P2,
						  reason=WinReason.TWO_CARAVANS if p2_wins == 2 else WinReason.THREE_CARAVANS,
						  end_turn_number=state.turn_number)

	raise InvalidOutcome(f"Invalid victory outcome: Both players won with P1: {p1_wins} and P2: {p2_wins}.")


def check_victory(state: GameState) -> GameResult | None:
	if _all_routes_closed(state):
		caravan_game_result = _get_caravan_sales_winner(state)

		if caravan_game_result is not None:
			return caravan_game_result

	return None

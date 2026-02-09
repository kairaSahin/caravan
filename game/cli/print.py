from game.caravan.caravan import Caravan
from game.caravan.enums import RouteId
from game.player.enums import PlayerId
from game.state.game_state import GameState, PlayerState


def _print_turn_number_phase_current_player(state: GameState) -> None:
	print(
		f"Turn: {state.turn_number} | Current Phase: {state.game_phase.get_name} | Current Player: P{state.current_player}")


def _get_caravan_pile_to_print(caravan: Caravan) -> str:
	pile_cards = list()

	for played_card in caravan.pile:
		base = played_card.base_card.get_name(full_name=False, suit_symbolized=True)

		if played_card.attachments:
			atts = ", ".join(att.get_name(full_name=False, suit_symbolized=True) for att in played_card.attachments)
			pile_cards.append(f"{base}[{atts}]")
		else:
			pile_cards.append(base)

	return " ".join(pile_cards)


def _print_route(state: GameState, route_id: RouteId) -> None:
	print(f"Route {route_id}:")

	p1 = state.get_caravan_by_route_player(PlayerId.P1, route_id)
	p2 = state.get_caravan_by_route_player(PlayerId.P2, route_id)

	if p1 is None or p2 is None:
		print("\t<route not initialized>")
		return

	(_, caravan_p1) = p1
	(_, caravan_p2) = p2

	print(
		f"\tP{PlayerId.P1} ({caravan_p1.score}): {_get_caravan_pile_to_print(caravan_p1) if caravan_p1.pile else '<empty>'}")
	print(
		f"\tP{PlayerId.P2} ({caravan_p2.score}): {_get_caravan_pile_to_print(caravan_p2) if caravan_p2.pile else '<empty>'}")


def _print_routes(state: GameState) -> None:
	for route_id in RouteId:
		_print_route(state, route_id)


def _print_player_hand_and_deck_count(player: PlayerState) -> None:
	print("Hand:")

	for i, card in enumerate(player.hand.values()):
		print(f"\t[{i}], {card.get_name(full_name=True, suit_symbolized=True)}")

	print(f"Deck: {len(player.deck)} cards")


def print_game_state(game_state: GameState):
	current_player = game_state.players.get(game_state.current_player)

	if current_player is None:
		print("<current player not found>")
		return

	_print_turn_number_phase_current_player(game_state)
	_print_routes(game_state)
	_print_player_hand_and_deck_count(current_player)

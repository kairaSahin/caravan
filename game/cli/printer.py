from game.caravan.caravan import Caravan
from game.caravan.enums import RouteId, CaravanId
from game.moves.types import Move, PlayCard, AttachFaceCard, DiscardCard, DiscardCaravan, Concede
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


def print_caravan_pile_with_indices(state: GameState, caravan_id: CaravanId) -> None:
	caravan = state.get_caravan(caravan_id)

	if caravan is None:
		print("<invalid caravan>")
		return

	if not caravan.pile:
		print("<caravan is empty>")
		return

	print(f"Choose a target base card:")
	for i, played_card in enumerate(caravan.pile):
		base = played_card.base_card.get_name(full_name=False, suit_symbolized=True)

		if played_card.attachments:
			atts = ", ".join(
				att.get_name(full_name=False, suit_symbolized=True)
				for att in played_card.attachments
			)
			print(f"\t[{i}] {base}[{atts}]")
		else:
			print(f"\t[{i}] {base}")


def _print_route(state: GameState, route_id: RouteId, with_ids=False) -> None:
	print(f"Route {route_id}:")

	p1 = state.get_caravan_by_route_player(PlayerId.P1, route_id)
	p2 = state.get_caravan_by_route_player(PlayerId.P2, route_id)

	if p1 is None or p2 is None:
		print("\t<route not initialized>")
		return

	(caravan_p1_id, caravan_p1) = p1
	(caravan_p2_id, caravan_p2) = p2

	p1_index = f"[{caravan_p1_id.value}] " if with_ids else ""
	p2_index = f"[{caravan_p2_id.value}] " if with_ids else ""

	print(
		f"\t{p1_index}P{PlayerId.P1} ({caravan_p1.score}): {_get_caravan_pile_to_print(caravan_p1) if caravan_p1.pile else '<empty>'}")
	print(
		f"\t{p2_index}P{PlayerId.P2} ({caravan_p2.score}): {_get_caravan_pile_to_print(caravan_p2) if caravan_p2.pile else '<empty>'}")


def print_routes(state: GameState, with_ids=False) -> None:
	for route_id in RouteId:
		_print_route(state, route_id, with_ids)


def print_player_hand_and_deck_count(player: PlayerState) -> None:
	print("Hand:")

	for i, card in enumerate(player.hand.values()):
		print(f"\t[{i}], {card.get_name(full_name=True, suit_symbolized=True)}")

	print(f"Deck: {len(player.deck)} cards")


def print_game_state(state: GameState):
	current_player = state.players.get(state.current_player)

	if current_player is None:
		print("<current player not found>")
		return

	_print_turn_number_phase_current_player(state)
	print_routes(state, False)
	print_player_hand_and_deck_count(current_player)


def print_applied_moves(state: GameState, move: Move) -> None:
	if isinstance(move, PlayCard):
		caravan_id = move.caravan_id
		caravan = state.get_caravan(caravan_id)

		base = next(
			(pc.base_card for pc in caravan.pile if pc.base_card.id == move.card_id),
			None
		)
		card_name = base.get_name(full_name=True, suit_symbolized=False) if base else "<unknown card>"

		print(f"P{move.player_id} played {card_name} on Caravan P{caravan_id.owner}.{caravan_id.route.value}")
	elif isinstance(move, AttachFaceCard):
		caravan = state.get_caravan(move.caravan_id)

		played = next(
			(pc for pc in caravan.pile if pc.base_card.id == move.target_base_id),
			None
		)
		target_name = played.base_card.get_name(full_name=True, suit_symbolized=False) if played else "<unknown target>"

		face = None
		if played is not None:
			face = next((fc for fc in played.attachments if fc.id == move.card_id), None)

		face_name = face.get_name(full_name=True, suit_symbolized=False) if face else "<unknown face card>"

		caravan_id = move.caravan_id
		print(
			f"P{move.player_id} played {face_name} on {target_name} in Caravan P{caravan_id.owner}.{caravan_id.route.value}")
	elif isinstance(move, DiscardCard):
		print(f"P{move.player_id} discarded a card")
	elif isinstance(move, DiscardCaravan):
		caravan_id = move.caravan_id

		print(f"P{move.player_id} discarded Caravan P{caravan_id.owner}.{caravan_id.route.value}")
	elif isinstance(move, Concede):
		print(f"P{move.player_id} conceded")


def print_error(_state: GameState, err: str) -> None:
	print(f"Illegal move: {err}")

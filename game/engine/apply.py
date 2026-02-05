from game.cards.enums import Rank
from game.engine.exceptions import IllegalMove
from game.engine.victory import check_victory
from game.moves.types import Move, PlayCard, AttachFaceCard, DiscardCard, DiscardCaravan, Concede
from game.player.enums import PlayerId
from game.rules.ruleset import can_play_base, can_attach_face, can_discard_card, can_discard_caravan, can_concede
from game.state.enums import GamePhase
from game.state.functions import get_move_player
from game.state.game_state import GameState, GameResult


def _draw_one_if_possible(state: GameState, move: Move) -> None:
	player = get_move_player(state, move)

	if not player.deck or state.game_phase == GamePhase.SETUP:
		# Players do not lose the game if their deck is empty, they just cannot draw anymore
		# A player losing due to having no cards left, i.e. empty hand and empty deck, is handled in "game.engine.victory.check_victory".
		return

	new_card = player.deck.pop()
	player.add_card_to_hand_card(new_card)


def _setup_complete_for_player(state: GameState, player_id: PlayerId) -> bool:
	# Should practically not occur as this should not be called if the game is not in setup mode
	# Added as failsafe.
	if state.game_phase != GamePhase.SETUP:
		return True

	for caravan_id, caravan in state.caravans.items():
		if caravan_id.owner == player_id and len(caravan.pile) == 0:
			return False

	return True


def _setup_complete_for_both(state: GameState) -> bool:
	return _setup_complete_for_player(state, PlayerId.P1) and _setup_complete_for_player(state, PlayerId.P2)


def _advance_after_play(state: GameState) -> None:
	if state.game_phase == GamePhase.SETUP:
		if _setup_complete_for_both(state):
			state.game_phase = GamePhase.MAIN

	state.turn_number += 1
	state.current_player = PlayerId.P2 if state.current_player == PlayerId.P1 else PlayerId.P1


def _resolve_jack_effect(state: GameState, move: AttachFaceCard) -> None:
	caravan = state.get_caravan(move.caravan_id)

	if not caravan:
		return

	caravan.remove_base_card(move.target_base_id)


def _resolve_joker_effect(state: GameState, move: AttachFaceCard) -> None:
	caravan = state.get_caravan(move.caravan_id)

	if not caravan:
		return

	target_played_card = next(
		(played_card for played_card in caravan.pile if played_card.base_card.id == move.target_base_id), None)

	if not target_played_card:
		return

	target_base_card = target_played_card.base_card

	if target_base_card.rank == Rank.ACE:
		suit_to_remove = target_base_card.suit

		for caravan in state.caravans.values():
			caravan.remove_base_cards_where(
				lambda card: (card.id != move.target_base_id) and (card.suit == suit_to_remove) and card.rank.is_numeric
			)

	else:
		rank_to_remove = target_base_card.rank

		for caravan in state.caravans.values():
			caravan.remove_base_cards_where(
				lambda card: (card.id != move.target_base_id) and (card.rank == rank_to_remove) and card.rank.is_numeric
			)


def _apply_play_base(state: GameState, move: PlayCard) -> GameResult | None:
	if not can_play_base(state, move):
		# TODO: Check raised errors later.
		raise IllegalMove("Play base move is not legal.")

	player = get_move_player(state, move)
	caravan = state.get_caravan(move.caravan_id)

	if player is None or caravan is None:
		# TODO: Check raised errors later.
		raise IllegalMove("Invalid player or caravan.")

	played_card = player.hand.pop(move.card_id)

	caravan.add_base_card(played_card)

	game_result = check_victory(state)

	if game_result is not None:
		return game_result

	_draw_one_if_possible(state, move)
	_advance_after_play(state)

	return None


def _apply_attach_face_card(state: GameState, move: AttachFaceCard) -> GameResult | None:
	if not can_attach_face(state, move):
		# TODO: Check raised errors later.
		raise IllegalMove("Attach face move is not legal.")

	player = get_move_player(state, move)
	caravan = state.get_caravan(move.caravan_id)

	if player is None or caravan is None:
		# TODO: Check raised errors later.
		raise IllegalMove("Invalid player or caravan.")

	face_card = player.hand.pop(move.card_id)

	caravan.attach(move.target_base_id, face_card)

	if face_card.rank == Rank.JACK:
		_resolve_jack_effect(state, move)

	elif face_card.rank == Rank.JOKER:
		_resolve_joker_effect(state, move)

	game_result = check_victory(state)

	if game_result is not None:
		return game_result

	_draw_one_if_possible(state, move)
	_advance_after_play(state)

	return None


def _apply_discard_card(state: GameState, move: DiscardCard) -> GameResult | None:
	if not can_discard_card(state, move):
		# TODO: Check raised errors later.
		raise IllegalMove("Discard card move is not legal.")

	player = get_move_player(state, move)

	if player is None:
		# TODO: Check raised errors later.
		raise IllegalMove("Invalid player.")

	player.hand.pop(move.card_id)

	game_result = check_victory(state)

	if game_result is not None:
		return game_result

	_draw_one_if_possible(state, move)
	_advance_after_play(state)

	return None


def _apply_discard_caravan(state: GameState, move: DiscardCaravan) -> GameResult | None:
	if not can_discard_caravan(state, move):
		# TODO: Check raised errors later.
		raise IllegalMove("Discard caravan move is not legal.")

	caravan = state.get_caravan(move.caravan_id)

	if caravan is None:
		# TODO: Check raised errors later.
		raise IllegalMove("Invalid caravan.")

	caravan.discard_caravan()

	game_result = check_victory(state)

	if game_result is not None:
		return game_result

	_advance_after_play(state)

	return None


def _apply_concede(state: GameState, move: Concede) -> GameResult | None:
	if not can_concede(state, move):
		# TODO: Check raised errors later.
		raise IllegalMove("Concede move is not legal.")

	game_result = check_victory(state, move)

	if game_result is not None:
		return game_result

	return None


def apply_move(state: GameState, move: Move) -> GameResult | None:
	if isinstance(move, PlayCard):
		game_result = _apply_play_base(state, move)
	elif isinstance(move, AttachFaceCard):
		game_result = _apply_attach_face_card(state, move)
	elif isinstance(move, DiscardCard):
		game_result = _apply_discard_card(state, move)
	elif isinstance(move, DiscardCaravan):
		game_result = _apply_discard_caravan(state, move)
	elif isinstance(move, Concede):
		game_result = _apply_concede(state, move)
	else:
		# TODO: Check raised errors later.
		raise IllegalMove(f"Unsupported move: {type(move).__name__}")

	return game_result

from game.cards.enums import Rank
from game.engine.exceptions import IllegalMove
from game.moves.types import Move, PlayCard, AttachFaceCard, DiscardCard, DiscardCaravan
from game.player.enums import PlayerId
from game.rules.ruleset import can_play_base, can_attach_face, can_discard_card, can_discard_caravan
from game.state.enums import GamePhase
from game.state.functions import get_move_player
from game.state.game_state import GameState


def _draw_one_if_possible(state: GameState, move: Move) -> None:
	player = get_move_player(state, move)

	if not player.deck or state.game_phase == GamePhase.SETUP:
		# FIXME: If a player's deck is empty, they will lose. However this may be implemented somewhere else.
		# FIXME: If the game is still in SETUP players do not draw new cards. This might also be implemented externally.
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


def _apply_play_base(state: GameState, move: PlayCard) -> None:
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

	_draw_one_if_possible(state, move)
	_advance_after_play(state)


def _apply_attach_face_card(state: GameState, move: AttachFaceCard) -> None:
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

	_draw_one_if_possible(state, move)
	_advance_after_play(state)


def _apply_discard_card(state: GameState, move: DiscardCard) -> None:
	if not can_discard_card(state, move):
		# TODO: Check raised errors later.
		raise IllegalMove("Discard card move is not legal.")

	player = get_move_player(state, move)

	if player is None:
		# TODO: Check raised errors later.
		raise IllegalMove("Invalid player.")

	player.hand.pop(move.card_id)

	_draw_one_if_possible(state, move)
	_advance_after_play(state)


def _apply_discard_caravan(state: GameState, move: DiscardCaravan) -> None:
	if not can_discard_caravan(state, move):
		# TODO: Check raised errors later.
		raise IllegalMove("Discard caravan move is not legal.")

	caravan = state.get_caravan(move.caravan_id)

	if caravan is None:
		# TODO: Check raised errors later.
		raise IllegalMove("Invalid caravan.")

	caravan.discard_caravan()

	_advance_after_play(state)


def apply_move(state: GameState, move: Move) -> None:
	if isinstance(move, PlayCard):
		_apply_play_base(state, move)
		return
	elif isinstance(move, AttachFaceCard):
		_apply_attach_face_card(state, move)
		return
	elif isinstance(move, DiscardCard):
		_apply_discard_card(state, move)
		return
	elif isinstance(move, DiscardCaravan):
		_apply_discard_caravan(state, move)
		return

	# TODO: Check raised errors later.
	raise IllegalMove(f"Unsupported move: {type(move).__name__}")

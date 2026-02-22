from uuid import UUID

from game.caravan.caravan import Caravan
from game.caravan.enums import CaravanId
from game.cards.card import PlayedCard, Card
from game.player.enums import PlayerId
from game.state.game_state import GameState, GameResult, PlayerState


def _game_result_to_payload(result: GameResult | None) -> dict | None:
	if result is None:
		return None

	return {
		"winner_id": result.winner_id,
		"end_turn_number": result.end_turn_number,
		"reason": result.reason.value,
	}


def _caravans_to_payload(caravans: dict[CaravanId, Caravan]) -> dict:
	return {caravan_id: _caravan_to_payload(caravan) for caravan_id, caravan in caravans.items()}


def _caravan_to_payload(caravan: Caravan) -> dict:
	return {
		"id": caravan.id.value,
		"pile": _pile_to_payload(caravan.pile),
	}


def _pile_to_payload(pile: list[PlayedCard]) -> list:
	return list(_played_card_to_payload(played_card) for played_card in pile)


def _played_card_to_payload(played_card: PlayedCard) -> dict:
	return {
		"base_card": _card_to_payload(played_card.base_card),
		"attachments": _attachments_to_payload(played_card.attachments)
	}


def _attachments_to_payload(attachments: list[Card]) -> list[dict]:
	return list(_card_to_payload(attachment) for attachment in attachments)


def _card_to_payload(card: Card) -> dict:
	return {
		"id": str(card.id),
		"rank": card.rank.value,
		"suit": card.suit.value if card.suit is not None else None,
	}


def _players_to_payload(players: dict[PlayerId, PlayerState]) -> dict:
	return {player_id: _player_to_payload(player) for player_id, player in players.items()}


def _player_to_payload(player: PlayerState) -> dict:
	return {
		"deck": _deck_to_payload(player.deck),
		"hand": _hand_to_payload(player.hand),
	}


def _deck_to_payload(deck: list[Card]) -> list:
	return list(_card_to_payload(card) for card in deck)


def _hand_to_payload(hand: dict[UUID, Card]) -> dict:
	return {str(card_id): _card_to_payload(card) for card_id, card in hand.items()}


def game_state_to_payload(state: GameState) -> dict:
	return {
		"players": _players_to_payload(state.players),
		"caravans": _caravans_to_payload(state.caravans),
		"current_player": state.current_player,
		"turn_number": state.turn_number,
		"game_phase": state.game_phase,
		"game_result": _game_result_to_payload(state.game_result)
	}

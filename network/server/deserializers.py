from uuid import UUID

from game.caravan.caravan import Caravan
from game.caravan.enums import CaravanId
from game.cards.card import Card, PlayedCard
from game.cards.enums import Suit, Rank
from game.player.enums import PlayerId
from game.state.enums import WinReason, GamePhase
from game.state.game_state import GameState, GameResult, PlayerState


def _payload_to_game_result(game_result: dict | None) -> GameResult | None:
	if game_result is None:
		return None

	return GameResult(
		winner_id=PlayerId(game_result['winner_id']),
		reason=WinReason(game_result['reason']) if game_result['reason'] is not None else None,
		end_turn_number=game_result['end_turn_number'],
	)


def _payload_to_current_player(player_id: int) -> PlayerId:
	return PlayerId(player_id)


def _payload_to_game_phase(game_phase: int) -> GamePhase:
	return GamePhase(game_phase)


def _payload_to_players(players: dict) -> dict[PlayerId, PlayerState]:
	# We wrap with `int()` here because in this dictionary the PlayerId is stored as a key so it is loaded as a string by `json.loads()`.
	return {PlayerId(int(player_id)): _payload_to_player(player) for player_id, player in players.items()}


def _payload_to_player(player: dict) -> PlayerState:
	return PlayerState(
		deck=_payload_to_deck(player['deck']),
		hand=_payload_to_hand(player['hand']),
	)


def _payload_to_deck(deck: list) -> list[Card]:
	return list(_payload_to_card(card) for card in deck)


def _payload_to_hand(hand: dict) -> dict[UUID, Card]:
	return {UUID(card_id): _payload_to_card(card) for card_id, card in hand.items()}


def _payload_to_card(card: dict) -> Card:
	return Card(
		id=UUID(card['id']),
		rank=Rank(card['rank']),
		suit=Suit(card['suit']) if card['suit'] is not None else None,

	)


def _payload_to_caravans(caravans: dict) -> dict[CaravanId, Caravan]:
	# We wrap with `int()` here because in this dictionary the CaravanId is stored as a key so it is loaded as a string by `json.loads()`.
	return {CaravanId(int(caravan_id)): _payload_to_caravan(caravan) for caravan_id, caravan in caravans.items()}


def _payload_to_caravan(caravan: dict) -> Caravan:
	return Caravan(
		id=CaravanId(caravan['id']),
		pile=_payload_to_pile(caravan['pile']),
	)


def _payload_to_pile(pile: list) -> list[PlayedCard]:
	return list(_payload_to_played_card(played_card) for played_card in pile)


def _payload_to_played_card(played_card: dict) -> PlayedCard:
	return PlayedCard(
		base_card=_payload_to_card(played_card['base_card']),
		attachments=_payload_attachments(played_card['attachments']),
	)


def _payload_attachments(attachments: list[dict]) -> list[Card]:
	return list(_payload_to_card(attachment) for attachment in attachments)


def payload_to_game_state(payload: dict[str, int | dict | None]) -> GameState:
	return GameState(
		players=_payload_to_players(payload['players']),
		caravans=_payload_to_caravans(payload['caravans']),
		current_player=_payload_to_current_player(payload['current_player']),
		turn_number=payload['turn_number'],
		game_phase=_payload_to_game_phase(payload['game_phase']),
		game_result=_payload_to_game_result(payload['game_result']),
	)

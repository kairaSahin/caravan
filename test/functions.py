from typing import overload
from uuid import uuid4

from game.caravan.caravan import Caravan
from game.caravan.enums import CaravanId
from game.cards.card import Card
from game.cards.enums import Rank, Suit
from game.moves.types import Move, PlayCard, AttachFaceCard, DiscardCard, DiscardCaravan, Concede
from game.player.enums import PlayerId
from game.state.enums import GamePhase
from game.state.game_state import PlayerState, GameState


def create_numeric_card(rank: Rank, suit: Suit | None) -> Card:
	return Card(id=uuid4(), rank=rank, suit=suit)


def create_player(deck: list[Card], hand: list[Card]) -> PlayerState:
	return PlayerState(deck=deck, hand={card.id: card for card in hand})


def initialise_caravans() -> dict:
	return {caravan_id: Caravan(id=caravan_id) for caravan_id in CaravanId}


def create_game_state(
		players: list[PlayerState],
		caravans: dict[CaravanId, Caravan],
		current_player: PlayerId,
		game_phase: GamePhase,
		turn_number: int) -> GameState:
	return GameState(players={PlayerId.P1: players[0], PlayerId.P2: players[1]},
					 caravans=caravans,
					 current_player=current_player,
					 game_phase=game_phase,
					 turn_number=turn_number)


@overload
def create_move(move_class: type[PlayCard], **kwargs) -> PlayCard: ...
@overload
def create_move(move_class: type[AttachFaceCard], **kwargs) -> AttachFaceCard: ...
@overload
def create_move(move_class: type[DiscardCard], **kwargs) -> DiscardCard: ...
@overload
def create_move(move_class: type[DiscardCaravan], **kwargs) -> DiscardCaravan: ...
@overload
def create_move(move_class: type[Concede], **kwargs) -> Concede: ...


def create_move(move_class: type[Move], **kwargs) -> Move:
	return move_class(**kwargs)

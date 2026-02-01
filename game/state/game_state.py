from dataclasses import dataclass
from uuid import UUID

from game.caravan.caravan import Caravan
from game.caravan.enums import CaravanId
from game.cards.card import Card
from game.player.enums import PlayerId
from game.state.enums import GamePhase


@dataclass
class PlayerState:
	deck: list[Card]
	hand: dict[UUID, Card]

	def get_card(self, card_id: UUID) -> Card | None:
		return self.hand.get(card_id)

	def add_card_to_hand_card(self, card) -> None:
		self.hand[card.id] = card


@dataclass
class GameState:
	players: dict[PlayerId, PlayerState]
	caravans: dict[CaravanId, Caravan]
	current_player: PlayerId
	turn_number: int
	game_phase: GamePhase

	def get_caravan(self, caravan_id: CaravanId) -> Caravan | None:
		return self.caravans.get(caravan_id)

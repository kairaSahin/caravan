from dataclasses import dataclass, field
from uuid import UUID

from game.caravan.caravan import Caravan
from game.caravan.enums import CaravanId, RouteId
from game.cards.card import Card
from game.player.enums import PlayerId
from game.state.enums import GamePhase, WinReason


@dataclass
class PlayerState:
	deck: list[Card]
	hand: dict[UUID, Card]

	def get_card(self, card_id: UUID) -> Card | None:
		return self.hand.get(card_id)

	def add_card_to_hand_card(self, card: Card) -> None:
		self.hand[card.id] = card


@dataclass
class GameResult:
	winner_id: PlayerId
	reason: WinReason
	end_turn_number: int


@dataclass
class GameState:
	players: dict[PlayerId, PlayerState]
	caravans: dict[CaravanId, Caravan]
	current_player: PlayerId
	turn_number: int
	game_phase: GamePhase
	game_result: GameResult | None = field(default=None)

	def get_caravan(self, caravan_id: CaravanId) -> Caravan | None:
		return self.caravans.get(caravan_id)

	def get_caravan_by_route_player(self, player_id: PlayerId, route_id: RouteId) -> tuple[CaravanId, Caravan] | None:
		for caravan_id, caravan in self.caravans.items():
			if caravan_id.route == route_id and caravan_id.owner == player_id:
				return caravan_id, caravan

		return None

from dataclasses import dataclass, field
from uuid import UUID

from game.cards.enums import Rank, Suit


# frozen=True, Card instances cannot change their values, modifications will not alter base values.
@dataclass(frozen=True)
class Card:
	id: UUID
	rank: Rank
	# 'None' for joker.
	suit: Suit | None

	@property
	def base_value(self) -> int:
		if not self.rank.is_numeric:
			# TODO: Check raised errors later.
			raise ValueError("Value fetched for non-numeric rank.")

		return self.rank.value

# TODO: Check on this later may change it 26.01.26
@dataclass()
class PlayedCard:
	base_card: Card
	attachments: list[Card] = field(default_factory=list)
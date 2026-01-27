from dataclasses import dataclass, field
from uuid import UUID

from game.cards.enums import Rank, Suit


# frozen=True, Card instances cannot change their values, modifications will not alter base values.
@dataclass(frozen=True)
class Card:
	id: UUID
	rank: Rank
	# 'None' for joker.
	suit: Suit

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

	# Count of queens is used to determine how the direction of the caravan is changed.
	# Odd queens change direction, even queens revert direction to its original state.
	@property
	def queen_count(self) -> int:
		return sum(1 for face_card in self.attachments if face_card.rank == Rank.QUEEN)

	@property
	def last_queen_suit(self) -> Suit:
		for face_card in reversed(self.attachments):
			if face_card.rank == Rank.QUEEN:
				return face_card.suit

		return None
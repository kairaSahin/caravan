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

	def get_name(self, full_name=False, suit_symbolized=True) -> str:
		rank_name = self.rank.get_full_name if full_name else self.rank.value

		if self.suit is not None:
			suit_name = self.suit.get_suit_symbol if suit_symbolized else f" of {self.suit.get_full_name}"
		else:
			suit_name = ""

		return f"{rank_name}{suit_name}"


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
	def last_queen_suit(self) -> Suit | None:
		for face_card in reversed(self.attachments):
			if face_card.rank == Rank.QUEEN:
				return face_card.suit

		return None

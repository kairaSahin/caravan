from enum import Enum


class Rank(Enum):
	ACE = 1
	TWO = 2
	THREE = 3
	FOUR = 4
	FIVE = 5
	SIX = 6
	SEVEN = 7
	EIGHT = 8
	NINE = 9
	TEN = 10

	KING = 'K'
	QUEEN = 'Q'
	JACK = 'J'
	JOKER = 'JK'

	@property
	def is_numeric(self) -> bool:
		return self in _NUMERIC_RANKS

	@property
	def is_face(self) -> bool:
		return self in _FACE_RANKS

	@property
	def get_full_name(self):
		if self in _FACE_RANKS:
			if self.value == Rank.JACK:
				return 'Jack'
			elif self.value == Rank.QUEEN:
				return 'Queen'
			elif self.value == Rank.KING:
				return 'King'
			else:
				return 'Spades'
		else:
			return self.value


_NUMERIC_RANKS = {
	Rank.ACE, Rank.TWO, Rank.THREE, Rank.FOUR, Rank.FIVE,
	Rank.SIX, Rank.SEVEN, Rank.EIGHT, Rank.NINE, Rank.TEN
}

_FACE_RANKS = {Rank.JACK, Rank.QUEEN, Rank.KING, Rank.JOKER}


class Suit(Enum):
	HEARTS = 'H'
	DIAMONDS = 'D'
	CLUBS = 'C'
	SPADES = 'S'

	@property
	def get_full_name(self):
		if self.value == Suit.HEARTS:
			return 'Hearts'
		elif self.value == Suit.DIAMONDS:
			return 'Diamonds'
		elif self.value == Suit.CLUBS:
			return 'Clubs'
		else:
			return 'Spades'

	@property
	def get_suit_symbol(self):
		if self.value == Suit.HEARTS:
			return '♥'
		elif self.value == Suit.DIAMONDS:
			return '♦'
		elif self.value == Suit.CLUBS:
			return '♣'
		else:
			return '♠'

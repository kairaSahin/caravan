from uuid import uuid4

from game.cards.card import Card
from game.cards.enums import Suit, Rank
from game.player.enums import PlayerId


def build_standard_deck(_: PlayerId) -> list[Card]:
	deck = list()

	for suit in Suit:
		for rank in Rank:
			if rank != Rank.JOKER:
				deck.append(Card(uuid4(), rank, suit))

	deck.append(Card(uuid4(), Rank.JOKER, None))
	deck.append(Card(uuid4(), Rank.JOKER, None))

	return deck

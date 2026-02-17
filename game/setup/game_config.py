from collections.abc import Callable
from dataclasses import dataclass, field

from numpy.random import Generator, default_rng

from game.cards.card import Card
from game.player.enums import PlayerId


@dataclass(frozen=True)
class GameConfig:
	deck_builder: Callable[[PlayerId], list[Card]]
	starting_hand_size: int = field(default=8)
	starting_player: PlayerId = field(default=PlayerId.P1)
	shuffle_decks: bool = field(default=True)
	random_generator: Generator = field(default_factory=default_rng)

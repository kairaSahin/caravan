from enum import IntEnum, Enum


class GamePhase(IntEnum):
	SETUP = 0
	MAIN = 1
	FINISHED = 2

	@property
	def get_name(self):
		if self == GamePhase.SETUP:
			return "Setup"
		if self == GamePhase.MAIN:
			return "Main"
		else:
			return "Finished"


class WinReason(Enum):
	TWO_CARAVANS = "two_caravans"
	THREE_CARAVANS = "three_caravans"
	CONCEDE = "concede"
	OUT_OF_CARDS = "out_of_cards"

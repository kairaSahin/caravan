from enum import Enum, IntEnum

from game.player.enums import PlayerId


class Direction(Enum):
	UNSET = 'unset'
	DESCENDING = 'descending'
	ASCENDING = 'ascending'


# Actual Caravan names from the game Boneyard, Redding, Shady Sands, Dayglow, New Reno, and The Hub.
class CaravanId(IntEnum):
	P1_A = 0
	P1_B = 1
	P1_C = 2
	P2_A = 3
	P2_B = 4
	P2_C = 5

	@property
	def owner(self) -> PlayerId:
		return PlayerId.P1 if self in {CaravanId.P1_A, CaravanId.P1_B, CaravanId.P1_C} else PlayerId.P2

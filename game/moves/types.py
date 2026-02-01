from dataclasses import dataclass, field
from enum import Enum
from uuid import UUID

from game.caravan.enums import CaravanId
from game.player.enums import PlayerId


class MoveType(Enum):
	PLAY_BASE = 'play_base'
	ATTACH_FACE = 'attach_face'
	DISCARD_CARD = 'discard_card'
	DISCARD_CARAVAN = 'discard_caravan'
	CONCEDE = 'concede'


# TODO: Check if more moves are possible.
@dataclass(frozen=True)
class Move:
	player_id: PlayerId
	move_type: MoveType = field(init=False)


@dataclass(frozen=True)
class PlayCard(Move):
	card_id: UUID
	caravan_id: CaravanId
	move_type: MoveType = field(init=False, default=MoveType.PLAY_BASE)


@dataclass(frozen=True)
class AttachFaceCard(Move):
	card_id: UUID
	caravan_id: CaravanId
	target_base_id: UUID
	move_type: MoveType = field(init=False, default=MoveType.ATTACH_FACE)


@dataclass(frozen=True)
class DiscardCard(Move):
	card_id: UUID
	move_type: MoveType = field(init=False, default=MoveType.DISCARD_CARD)


@dataclass(frozen=True)
class DiscardCaravan(Move):
	caravan_id: CaravanId
	move_type: MoveType = field(init=False, default=MoveType.DISCARD_CARAVAN)


@dataclass(frozen=True)
class Concede(Move):
	move_type: MoveType = field(init=False, default=MoveType.CONCEDE)

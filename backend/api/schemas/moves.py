from typing import Annotated, Literal, Union
from uuid import UUID

from pydantic import BaseModel, Field

from game.caravan.enums import CaravanId
from game.moves.types import (
	AttachFaceCard,
	Concede,
	DiscardCard,
	DiscardCaravan,
	Move,
	MoveType,
	PlayCard,
)
from game.player.enums import PlayerId


class PlayBaseMoveRequest(BaseModel):
	move_type: Literal[MoveType.PLAY_BASE]
	card_id: UUID
	caravan_id: CaravanId


class AttachFaceMoveRequest(BaseModel):
	move_type: Literal[MoveType.ATTACH_FACE]
	card_id: UUID
	caravan_id: CaravanId
	target_base_id: UUID


class DiscardCardMoveRequest(BaseModel):
	move_type: Literal[MoveType.DISCARD_CARD]
	card_id: UUID


class DiscardCaravanMoveRequest(BaseModel):
	move_type: Literal[MoveType.DISCARD_CARAVAN]
	caravan_id: CaravanId


class ConcedeMoveRequest(BaseModel):
	move_type: Literal[MoveType.CONCEDE]


MoveRequest = Annotated[
	Union[
		PlayBaseMoveRequest,
		AttachFaceMoveRequest,
		DiscardCardMoveRequest,
		DiscardCaravanMoveRequest,
		ConcedeMoveRequest,
	],
	Field(discriminator="move_type"),
]


def to_domain_move(req: MoveRequest, player_id: PlayerId) -> Move:
	if isinstance(req, PlayBaseMoveRequest):
		return PlayCard(player_id=player_id, card_id=req.card_id,
						caravan_id=req.caravan_id)
	if isinstance(req, AttachFaceMoveRequest):
		return AttachFaceCard(
			player_id=player_id,
			card_id=req.card_id,
			caravan_id=req.caravan_id,
			target_base_id=req.target_base_id,
		)
	if isinstance(req, DiscardCardMoveRequest):
		return DiscardCard(player_id=player_id, card_id=req.card_id)
	if isinstance(req, DiscardCaravanMoveRequest):
		return DiscardCaravan(player_id=player_id,
							  caravan_id=req.caravan_id)
	return Concede(player_id=player_id)

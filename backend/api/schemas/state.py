from pydantic import BaseModel, Field

from game.caravan.enums import CaravanId
from game.player.enums import PlayerId
from game.state.enums import GamePhase


class CardPayload(BaseModel):
	id: str
	rank: int | str
	suit: str | None = None


class PlayedCardPayload(BaseModel):
	base_card: CardPayload
	attachments: list[CardPayload]


class CaravanPayload(BaseModel):
	id: int
	pile: list[PlayedCardPayload]


class PlayerPayload(BaseModel):
	deck: list[CardPayload]
	hand: dict[str, CardPayload]


class OpponentPayload(BaseModel):
	deck_size: int = Field(ge=0)
	hand_size: int = Field(ge=0)


class GameResultPayload(BaseModel):
	winner_id: PlayerId
	end_turn_number: int = Field(ge=0)
	reason: str


class GameStateBasePayload(BaseModel):
	caravans: dict[CaravanId, CaravanPayload]
	current_player: PlayerId
	turn_number: int = Field(ge=0)
	game_phase: GamePhase
	game_result: GameResultPayload | None = None


class GameStatePayload(GameStateBasePayload):
	players: dict[PlayerId, PlayerPayload]


class GameStateResponse(GameStatePayload):
	game_id: str
	state_version: int = Field(ge=0)


class GameStatePlayerExclusivePayload(GameStateBasePayload):
	player: PlayerPayload
	opponent: OpponentPayload


class GameStatePlayerExclusiveResponse(GameStatePlayerExclusivePayload):
	game_id: str
	state_version: int = Field(ge=0)

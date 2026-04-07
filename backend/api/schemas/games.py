from pydantic import BaseModel, model_validator

from backend.api.enums import DeckType, GameStatus, PlayerSlotStatus


class HostGameResponse(BaseModel):
	game_id: str
	join_code: str
	token: str


class GameRow(BaseModel):
	game_id: str
	join_code: str
	status: GameStatus
	player_1_status: PlayerSlotStatus
	player_2_status: PlayerSlotStatus
	player_1_ready: bool = False
	player_2_ready: bool = False
	player_1_deck_type: DeckType | None = None
	player_2_deck_type: DeckType | None = None
	player_1_deck_id: str | None = None
	player_2_deck_id: str | None = None
	started_at: str | None = None
	ended_at: str | None = None


class ReadyGameRequest(BaseModel):
	deck_type: DeckType
	deck_id: str | None = None

	@model_validator(mode='after')
	def validate_deck_fields(self):
		if self.deck_type is DeckType.STANDARD and self.deck_id is not None:
			raise ValueError("Deck ID cannot be used with standard decks")
		if self.deck_type is DeckType.CUSTOM and self.deck_id is None:
			raise ValueError("Deck ID is required for custom decks")

		return self

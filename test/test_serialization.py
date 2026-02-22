import json
from typing import Callable, Any

from game.player.enums import PlayerId
from game.setup.deck_builder import build_standard_deck
from game.setup.game_config import GameConfig
from numpy.random import default_rng

from game.setup.game_initializer import init_game
from game.state.enums import WinReason, GamePhase
from game.state.game_state import GameResult, GameState

# noinspection PyProtectedMember
from network.server.serializers import _game_result_to_payload
# noinspection PyProtectedMember
from network.server.deserializers import _payload_to_game_result, _payload_to_current_player, _payload_to_game_phase


def _init_game_state() -> GameState:
	game_config = GameConfig(
		deck_builder=build_standard_deck,
		starting_hand_size=8,
		starting_player=PlayerId.P1,
		shuffle_decks=True,
		random_generator=default_rng(42)
	)

	return init_game(game_config)


def _serialize_deserialize(deserializer: Callable[[dict | int], PlayerId | GameResult | GamePhase] | None,
						   serializer: Callable[[Any], dict] | None,
						   obj: object) -> PlayerId | GameResult | GamePhase:
	if serializer is not None:
		obj_to_dumps = serializer(obj)

	else:
		obj_to_dumps = obj

	dumped_loaded_obj = json.loads(json.dumps(obj_to_dumps))

	if deserializer is not None:
		return deserializer(dumped_loaded_obj)

	else:
		return dumped_loaded_obj


def test_game_result_serialization() -> None:
	state = _init_game_state()

	state.game_result = GameResult(winner_id=PlayerId.P2,
								   reason=WinReason.TWO_CARAVANS,
								   end_turn_number=state.turn_number)

	deserialized_game_result = _serialize_deserialize(_payload_to_game_result, _game_result_to_payload,
													  state.game_result)

	# Assert the serialized and deserialized game result stays the same.
	assert state.game_result == deserialized_game_result


def test_none_game_result_serialization() -> None:
	state = _init_game_state()

	deserialized_game_result = _serialize_deserialize(_payload_to_game_result, _game_result_to_payload,
													  state.game_result)

	# Assert the serialized and deserialized None game result stays the same.
	assert state.game_result == deserialized_game_result


def test_current_player_serialization() -> None:
	state = _init_game_state()

	deserialized_current_player = _serialize_deserialize(_payload_to_current_player, None, state.current_player)

	# Assert the serialized and deserialized current player stays the same.
	assert state.current_player == deserialized_current_player


def test_game_phase_serialization() -> None:
	state = _init_game_state()

	deserialized_game_phase = _serialize_deserialize(_payload_to_game_phase, None, state.game_phase)

	# Assert the serialized and deserialized game phase stays the same.
	assert state.game_phase == deserialized_game_phase
	# Assert the serialized and deserialized game phase is a proper enum with callables that return correct values.
	assert deserialized_game_phase.name == state.game_phase.name


def test_turn_number_serialization() -> None:
	state = _init_game_state()

	deserialized_turn_number = _serialize_deserialize(None, None, state.turn_number)

	# Assert the serialized and deserialized turn number stays the same.
	assert state.turn_number == deserialized_turn_number

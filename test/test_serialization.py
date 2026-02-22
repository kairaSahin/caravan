import json
from typing import Callable

from game.caravan.caravan import Caravan
from game.caravan.enums import CaravanId
from game.cards.enums import Rank, Suit
from game.player.enums import PlayerId
from game.setup.deck_builder import build_standard_deck
from game.setup.game_config import GameConfig
from numpy.random import default_rng

from game.setup.game_initializer import init_game
from game.state.enums import WinReason, GamePhase
from game.state.game_state import GameResult, GameState, PlayerState

# noinspection PyProtectedMember
from network.server.serializers import _game_result_to_payload, _players_to_payload
# noinspection PyProtectedMember
from network.server.deserializers import _payload_to_game_result, _payload_to_current_player, _payload_to_game_phase, \
	_payload_to_players
from test.functions import create_numeric_card


def _init_game_state() -> GameState:
	game_config = GameConfig(
		deck_builder=build_standard_deck,
		starting_hand_size=8,
		starting_player=PlayerId.P1,
		shuffle_decks=True,
		random_generator=default_rng(42)
	)

	return init_game(game_config)


type _TStateAttributes = PlayerId | GameResult | GamePhase | int | dict[PlayerId, PlayerState] | dict[
	CaravanId, Caravan]


def _serialize_deserialize(
		deserializer: Callable[[dict | int | None], _TStateAttributes] | None,
		serializer: Callable[[_TStateAttributes], dict | None] | None,
		obj: _TStateAttributes) -> _TStateAttributes:
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


def test_players_serialization() -> None:
	state = _init_game_state()

	deserialized_players = _serialize_deserialize(_payload_to_players, _players_to_payload, state.players)

	# Assert the serialized and deserialized players stays the same.
	assert state.players == deserialized_players
	# Assert a single player stays the same and is fetchable.
	assert state.players[PlayerId.P1] == deserialized_players[PlayerId.P1]

	# Assert that functions of PlayerState are usable.
	card = create_numeric_card(Rank.ACE, Suit.HEARTS)
	deserialized_players[PlayerId.P1].add_card_to_hand_card(card)

	assert deserialized_players[PlayerId.P1].hand[card.id] == card

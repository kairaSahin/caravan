import json
from typing import Callable, TypeVar

from game.caravan.enums import CaravanId
from game.cards.enums import Rank, Suit
from game.player.enums import PlayerId
from game.setup.deck_builder import build_standard_deck
from game.setup.game_config import GameConfig
from numpy.random import default_rng

from game.setup.game_initializer import init_game
from game.state.enums import WinReason
from game.state.game_state import GameResult, GameState

# noinspection PyProtectedMember
from network.server.serializers import _game_result_to_payload, _players_to_payload, _caravans_to_payload, \
	game_state_to_payload
# noinspection PyProtectedMember
from network.server.deserializers import _payload_to_game_result, _payload_to_current_player, _payload_to_game_phase, \
	_payload_to_players, _payload_to_caravans, payload_to_game_state
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


_TStateAttributes = TypeVar("_TStateAttributes")
_TSerializationDeserializationParams = dict | int | None


def _serialize_deserialize(
		deserializer: Callable[[_TSerializationDeserializationParams], _TStateAttributes] | None,
		serializer: Callable[[_TStateAttributes], _TSerializationDeserializationParams] | None,
		obj: _TStateAttributes,
) -> _TStateAttributes:
	obj_to_dumps = serializer(obj) if serializer is not None else obj
	dumped_loaded_obj = json.loads(json.dumps(obj_to_dumps))

	return deserializer(dumped_loaded_obj) if deserializer is not None else dumped_loaded_obj


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

	# Assert the serialized and deserialized players stay the same.
	assert state.players == deserialized_players
	# Assert a single player stays the same and is fetchable.
	assert state.players[PlayerId.P1] == deserialized_players[PlayerId.P1]

	# Assert that functions of PlayerState are usable.
	card = create_numeric_card(Rank.ACE, Suit.HEARTS)
	deserialized_players[PlayerId.P1].add_card_to_hand_card(card)

	assert deserialized_players[PlayerId.P1].hand[card.id] == card


def test_caravans_serialization() -> None:
	state = _init_game_state()

	deserialized_caravans = _serialize_deserialize(_payload_to_caravans, _caravans_to_payload, state.caravans)

	# Assert the serialized and deserialized caravans stay the same.
	assert state.caravans == deserialized_caravans
	# Assert a single caravan stays the same and is fetchable.
	assert state.caravans[CaravanId.P1_B] == deserialized_caravans[CaravanId.P1_B]
	# Assert that functions of CaravanId and Caravan are usable.
	card = create_numeric_card(Rank.ACE, Suit.HEARTS)
	deserialized_caravans[CaravanId.P1_B].add_base_card(card)

	assert deserialized_caravans[CaravanId.P1_B].pile[-1].base_card == card

	card_2 = create_numeric_card(Rank.QUEEN, Suit.DIAMONDS)
	deserialized_caravans[CaravanId.P1_B].attach(card.id, card_2)

	assert deserialized_caravans[CaravanId.P1_B].pile[-1].attachments[-1] == card_2

	assert deserialized_caravans[CaravanId.P1_B].id.owner == PlayerId.P1


def test_game_state_serialization() -> None:
	state = _init_game_state()

	deserialized_game_state = _serialize_deserialize(payload_to_game_state, game_state_to_payload, state)

	# Assert the serialized and deserialized game state stays the same.
	assert state == deserialized_game_state

	state.game_result = GameResult(winner_id=PlayerId.P2,
								   reason=WinReason.TWO_CARAVANS,
								   end_turn_number=state.turn_number)

	deserialized_game_state = _serialize_deserialize(payload_to_game_state, game_state_to_payload, state)

	# Assert the serialized and deserialized game state, with a game result, stays the same.
	assert state == deserialized_game_state

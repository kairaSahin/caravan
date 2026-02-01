import pytest

from game.caravan.enums import CaravanId, Direction
from game.cards.enums import Rank, Suit
from game.engine.apply import apply_move
from game.engine.exceptions import IllegalMove
from game.moves.types import PlayCard, DiscardCard, AttachFaceCard
from game.player.enums import PlayerId
from game.state.enums import GamePhase
from test.functions import create_numeric_card, create_player, initialise_caravans, create_game_state, create_move


def test_can_play_base_and_increase_caravan_score() -> None:
	hand_card = create_numeric_card(Rank.EIGHT, Suit.HEARTS)
	deck_card = create_numeric_card(Rank.FIVE, Suit.HEARTS)

	player_1 = create_player([deck_card], [hand_card])
	player_2 = create_player([], [])

	caravans = initialise_caravans()

	caravan_to_play = CaravanId.P1_A
	player_to_play = PlayerId.P1

	game_state = create_game_state(
		players=[player_1, player_2],
		caravans=caravans,
		current_player=player_to_play,
		game_phase=GamePhase.MAIN,
		turn_number=0
	)

	play_base_move = create_move(
		PlayCard,
		player_id=player_to_play,
		card_id=hand_card.id,
		caravan_id=caravan_to_play,
	)
	caravan = game_state.get_caravan(caravan_to_play)

	# Assert that Player 1 holds the card in their hand
	assert hand_card.id in game_state.players[player_to_play].hand
	# Assert that Player 1 holds one card in their deck
	assert len(game_state.players[player_to_play].deck) == 1
	# Assert that Player 1's 1st caravan is empty
	assert len(game_state.get_caravan(caravan_to_play).pile) == 0
	# Assert that the caravan has a score of "0"
	assert caravan.score == 0

	apply_move(game_state, play_base_move)

	# Assert that the played card is no longer is in Player 1's hand
	assert hand_card.id not in game_state.players[player_to_play].hand

	# Assert that the played card has been successfully added to the caravan and increase the score by its rank
	assert len(caravan.pile) == 1
	assert caravan.pile[-1].base_card.id == hand_card.id
	assert caravan.score == hand_card.rank.value

	# Assert that Player 1 has drawn the next card in their deck to their hand and that their deck is now empty
	assert deck_card.id in game_state.players[player_to_play].hand
	assert len(game_state.players[player_to_play].deck) == 0

	# Assert that the turn has successfully progressed
	assert game_state.current_player == PlayerId.P2
	assert game_state.turn_number == 1


def test_can_discard_card() -> None:
	hand_card = create_numeric_card(Rank.EIGHT, Suit.HEARTS)
	deck_card = create_numeric_card(Rank.FIVE, Suit.HEARTS)

	player_1 = create_player([deck_card], [hand_card])
	player_2 = create_player([], [])

	caravans = initialise_caravans()

	player_to_play = PlayerId.P1

	game_state = create_game_state(
		players=[player_1, player_2],
		caravans=caravans,
		current_player=player_to_play,
		game_phase=GamePhase.MAIN,
		turn_number=0
	)

	discard_card_move = create_move(
		DiscardCard,
		player_id=player_to_play,
		card_id=hand_card.id,
	)

	# Assert that Player 1 holds the card in their hand
	assert hand_card.id in game_state.players[player_to_play].hand
	# Assert that Player 1 holds one card in their deck
	assert len(game_state.players[player_to_play].deck) == 1

	apply_move(game_state, discard_card_move)

	# Assert that the played card is no longer is in Player 1's hand
	assert hand_card.id not in game_state.players[player_to_play].hand

	# Assert that all caravans are still empty
	assert all([len(caravan.pile) == 0 for caravan in caravans.values()])

	# Assert that Player 1 has drawn the next card in their deck to their hand and that their deck is now empty
	assert deck_card.id in game_state.players[player_to_play].hand
	assert len(game_state.players[player_to_play].deck) == 0

	# Assert that the turn has successfully progressed
	assert game_state.current_player == PlayerId.P2
	assert game_state.turn_number == 1


def test_cannot_discard_card_deck_empty() -> None:
	hand_card = create_numeric_card(Rank.EIGHT, Suit.HEARTS)

	player_1 = create_player([], [hand_card])
	player_2 = create_player([], [])

	caravans = initialise_caravans()

	player_to_play = PlayerId.P1

	game_state = create_game_state(
		players=[player_1, player_2],
		caravans=caravans,
		current_player=player_to_play,
		game_phase=GamePhase.MAIN,
		turn_number=0
	)

	discard_card_move = create_move(
		DiscardCard,
		player_id=player_to_play,
		card_id=hand_card.id,
	)

	# Assert that the card in a player's hand cannot be discarded as they have no cards left in their deck
	with pytest.raises(IllegalMove):
		apply_move(game_state, discard_card_move)

	# Assert that the turn has not successfully progressed
	assert game_state.current_player == PlayerId.P1
	assert game_state.turn_number == 0


def test_attach_king() -> None:
	hand_card = create_numeric_card(Rank.KING, Suit.HEARTS)
	deck_card = create_numeric_card(Rank.FIVE, Suit.HEARTS)
	caravan_card = create_numeric_card(Rank.TEN, Suit.HEARTS)

	player_1 = create_player([deck_card], [hand_card])
	player_2 = create_player([], [])

	caravans = initialise_caravans()

	caravan_to_play = CaravanId.P1_A
	player_to_play = PlayerId.P1

	game_state = create_game_state(
		players=[player_1, player_2],
		caravans=caravans,
		current_player=player_to_play,
		game_phase=GamePhase.MAIN,
		turn_number=0
	)
	attach_face_move = create_move(
		AttachFaceCard,
		player_id=player_to_play,
		card_id=hand_card.id,
		target_base_id=caravan_card.id,
		caravan_id=caravan_to_play,
	)
	caravan = game_state.get_caravan(caravan_to_play)
	caravan.add_base_card(caravan_card)

	# Assert that caravan only has a score of already placed card
	assert caravan.score == caravan_card.rank.value

	apply_move(game_state, attach_face_move)

	# Assert that the face card has been properly attached to the base card
	assert hand_card in caravan.pile[-1].attachments
	# Assert that pile length remains unchanged after face card attachment
	assert len(caravan.pile) == 1
	# Assert that score has doubled after King attachment
	assert caravan.score == caravan_card.rank.value * 2

	# Assert that the turn has successfully progressed
	assert game_state.current_player == PlayerId.P2
	assert game_state.turn_number == 1


def test_attach_queen() -> None:
	hand_card = create_numeric_card(Rank.QUEEN, Suit.DIAMONDS)
	deck_card = create_numeric_card(Rank.FIVE, Suit.HEARTS)
	caravan_card = create_numeric_card(Rank.TEN, Suit.HEARTS)
	caravan_card_2 = create_numeric_card(Rank.THREE, Suit.SPADES)

	player_1 = create_player([deck_card], [hand_card])
	player_2 = create_player([], [])

	caravans = initialise_caravans()

	caravan_to_play = CaravanId.P1_A
	player_to_play = PlayerId.P1

	game_state = create_game_state(
		players=[player_1, player_2],
		caravans=caravans,
		current_player=player_to_play,
		game_phase=GamePhase.MAIN,
		turn_number=0
	)
	attach_face_move = create_move(
		AttachFaceCard,
		player_id=player_to_play,
		card_id=hand_card.id,
		target_base_id=caravan_card_2.id,
		caravan_id=caravan_to_play,
	)
	caravan = game_state.get_caravan(caravan_to_play)
	caravan.add_base_card(caravan_card)
	caravan.add_base_card(caravan_card_2)

	# Assert that the direction of the caravan is currently descending 10 > 3
	assert caravan.direction == Direction.DESCENDING
	# Assert that the suit of the caravan is currently Spades
	assert caravan.current_suit == Suit.SPADES

	apply_move(game_state, attach_face_move)

	# Assert that the face card has been properly attached to the base card
	assert hand_card in caravan.pile[-1].attachments
	# Assert that pile length remains unchanged after face card attachment
	assert len(caravan.pile) == 2

	# Assert that the direction of the caravan has reversed from descending to ascending
	assert caravan.direction == Direction.ASCENDING
	# Assert that the current suit of the caravan has changed to the suit of the Queen; Diamonds
	assert caravan.current_suit == Suit.DIAMONDS

	# Assert that the turn has successfully progressed
	assert game_state.current_player == PlayerId.P2
	assert game_state.turn_number == 1


def test_attach_queen_direction_unset() -> None:
	hand_card = create_numeric_card(Rank.QUEEN, Suit.DIAMONDS)
	deck_card = create_numeric_card(Rank.FIVE, Suit.HEARTS)
	caravan_card = create_numeric_card(Rank.TEN, Suit.HEARTS)

	player_1 = create_player([deck_card], [hand_card])
	player_2 = create_player([], [])

	caravans = initialise_caravans()

	caravan_to_play = CaravanId.P1_A
	player_to_play = PlayerId.P1

	game_state = create_game_state(
		players=[player_1, player_2],
		caravans=caravans,
		current_player=player_to_play,
		game_phase=GamePhase.MAIN,
		turn_number=0
	)
	attach_face_move = create_move(
		AttachFaceCard,
		player_id=player_to_play,
		card_id=hand_card.id,
		target_base_id=caravan_card.id,
		caravan_id=caravan_to_play,
	)
	caravan = game_state.get_caravan(caravan_to_play)
	caravan.add_base_card(caravan_card)

	# Assert that the direction of the caravan is currently Unset as there is only one card
	assert caravan.direction == Direction.UNSET
	# Assert that the suit of the caravan is currently Hearts
	assert caravan.current_suit == Suit.HEARTS

	apply_move(game_state, attach_face_move)

	# Assert that the face card has been properly attached to the base card
	assert hand_card in caravan.pile[-1].attachments
	# Assert that pile length remains unchanged after face card attachment
	assert len(caravan.pile) == 1

	# Assert that the direction of the caravan is still Unset as there is still one numeric card
	assert caravan.direction == Direction.UNSET
	# Assert that the current suit of the caravan has changed to the suit of the Queen; Diamonds
	assert caravan.current_suit == Suit.DIAMONDS

	# Assert that the turn has successfully progressed
	assert game_state.current_player == PlayerId.P2
	assert game_state.turn_number == 1


def test_attach_jack() -> None:
	hand_card = create_numeric_card(Rank.JACK, Suit.DIAMONDS)
	deck_card = create_numeric_card(Rank.FIVE, Suit.HEARTS)
	caravan_card = create_numeric_card(Rank.TEN, Suit.HEARTS)

	player_1 = create_player([deck_card], [hand_card])
	player_2 = create_player([], [])

	caravans = initialise_caravans()

	caravan_to_play = CaravanId.P1_A
	player_to_play = PlayerId.P1

	game_state = create_game_state(
		players=[player_1, player_2],
		caravans=caravans,
		current_player=player_to_play,
		game_phase=GamePhase.MAIN,
		turn_number=0
	)
	attach_face_move = create_move(
		AttachFaceCard,
		player_id=player_to_play,
		card_id=hand_card.id,
		target_base_id=caravan_card.id,
		caravan_id=caravan_to_play,
	)
	caravan = game_state.get_caravan(caravan_to_play)
	caravan.add_base_card(caravan_card)

	# Assert that caravan only has a score of already placed card
	assert caravan.score == caravan_card.rank.value

	apply_move(game_state, attach_face_move)

	# Assert that the base card attached with Jack has been removed
	assert len(caravan.pile) == 0
	# Assert that score decreased due to removed card
	assert caravan.score == 0

	# Assert that the turn has successfully progressed
	assert game_state.current_player == PlayerId.P2
	assert game_state.turn_number == 1


def test_attach_jack_on_king_attached_base() -> None:
	hand_card = create_numeric_card(Rank.JACK, Suit.DIAMONDS)
	deck_card = create_numeric_card(Rank.FIVE, Suit.HEARTS)
	caravan_card = create_numeric_card(Rank.TEN, Suit.HEARTS)
	caravan_card_2 = create_numeric_card(Rank.SIX, Suit.SPADES)
	caravan_king_card = create_numeric_card(Rank.KING, Suit.HEARTS)

	player_1 = create_player([deck_card], [hand_card])
	player_2 = create_player([], [])

	caravans = initialise_caravans()

	caravan_to_play = CaravanId.P1_A
	player_to_play = PlayerId.P1

	game_state = create_game_state(
		players=[player_1, player_2],
		caravans=caravans,
		current_player=player_to_play,
		game_phase=GamePhase.MAIN,
		turn_number=0
	)
	attach_face_move = create_move(
		AttachFaceCard,
		player_id=player_to_play,
		card_id=hand_card.id,
		target_base_id=caravan_card_2.id,
		caravan_id=caravan_to_play,
	)
	caravan = game_state.get_caravan(caravan_to_play)
	caravan.add_base_card(caravan_card)
	caravan.add_base_card(caravan_card_2)
	caravan.attach(caravan_card_2.id, caravan_king_card)

	# Assert that caravan only has a score of already placed card
	assert caravan.score == caravan_card.rank.value + (caravan_card_2.rank.value * 2)
	# Assert that the caravan has a direction of Descending, 10 > 6
	assert caravan.direction == Direction.DESCENDING
	# Assert that the suit of the caravan is of the last card; Spades
	assert caravan.current_suit == Suit.SPADES

	apply_move(game_state, attach_face_move)

	# Assert that the base card attached with Jack has been removed
	assert len(caravan.pile) == 1
	# Assert that score decreased due to removed card
	assert caravan.score == caravan_card.rank.value
	# Assert that the direction of the caravan has successfully changed to Unset due to only card being left
	assert caravan.direction == Direction.UNSET
	# Assert that the suit of the caravan has changed to the remaining card; Hearts
	assert caravan.current_suit == Suit.HEARTS

	# Assert that the turn has successfully progressed
	assert game_state.current_player == PlayerId.P2
	assert game_state.turn_number == 1

# TODO: Add multiple attach face card tests!

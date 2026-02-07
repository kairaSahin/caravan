from game.caravan.enums import CaravanId
from game.cards.enums import Rank, Suit
from game.engine.apply import apply_move
from game.moves.types import Concede, PlayCard
from game.player.enums import PlayerId
from game.state.enums import GamePhase, WinReason
from game.state.game_state import GameResult
from test.functions import create_player, initialise_caravans, create_game_state, create_move, create_numeric_card


def test_concede_victory():
	player_1 = create_player([], [])
	player_2 = create_player([], [])

	caravans = initialise_caravans()

	player_to_play = PlayerId.P1
	winning_player = PlayerId.P2
	turn_number = 7

	game_state = create_game_state(
		players=[player_1, player_2],
		caravans=caravans,
		current_player=player_to_play,
		game_phase=GamePhase.MAIN,
		turn_number=turn_number
	)

	concede_move = create_move(
		Concede,
		player_id=player_to_play,
	)

	game_result = apply_move(game_state, concede_move)

	# Assert that the other player won on the turn of the conceding was initiated with Concede reason
	assert game_result == GameResult(
		winner_id=winning_player,
		reason=WinReason.CONCEDE,
		end_turn_number=turn_number
	)


def test_out_of_cards_victory():
	hand_card = create_numeric_card(Rank.EIGHT, Suit.HEARTS)
	deck_card = create_numeric_card(Rank.FIVE, Suit.HEARTS)

	player_1 = create_player([], [hand_card])
	player_2 = create_player([deck_card], [])

	caravans = initialise_caravans()

	caravan_to_play = CaravanId.P1_A
	player_to_play = PlayerId.P1
	winning_player = PlayerId.P2
	turn_number = 19

	game_state = create_game_state(
		players=[player_1, player_2],
		caravans=caravans,
		current_player=player_to_play,
		game_phase=GamePhase.MAIN,
		turn_number=turn_number
	)

	play_base_move = create_move(
		PlayCard,
		player_id=player_to_play,
		card_id=hand_card.id,
		caravan_id=caravan_to_play,
	)

	game_result = apply_move(game_state, play_base_move)

	# Assert that player 1 has run out of cards after their last move
	assert len(player_1.hand) == 0
	assert len(player_1.deck) == 0

	# Assert that player 1 lost due to running out of all their cards
	assert game_result == GameResult(
		winner_id=winning_player,
		reason=WinReason.OUT_OF_CARDS,
		end_turn_number=turn_number
	)


def test_three_caravan_sales_victory():
	hand_card = create_numeric_card(Rank.EIGHT, Suit.HEARTS)
	hand_card_p2 = create_numeric_card(Rank.EIGHT, Suit.HEARTS)
	deck_card = create_numeric_card(Rank.FIVE, Suit.HEARTS)

	player_1 = create_player([deck_card], [hand_card])
	player_2 = create_player([], [hand_card_p2])

	caravans = initialise_caravans()

	caravan_to_play = CaravanId.P1_A
	player_to_play = PlayerId.P1
	turn_number = 19

	game_state = create_game_state(
		players=[player_1, player_2],
		caravans=caravans,
		current_player=player_to_play,
		game_phase=GamePhase.MAIN,
		turn_number=turn_number
	)

	play_base_move = create_move(
		PlayCard,
		player_id=player_to_play,
		card_id=hand_card.id,
		caravan_id=caravan_to_play,
	)
	caravan = game_state.get_caravan(caravan_to_play)
	caravan_2 = game_state.get_caravan(CaravanId.P1_B)
	caravan_3 = game_state.get_caravan(CaravanId.P1_C)

	caravan.add_base_card(create_numeric_card(Rank.EIGHT, Suit.HEARTS))
	caravan.add_base_card(create_numeric_card(Rank.FIVE, Suit.HEARTS))
	caravan_2.add_base_card(create_numeric_card(Rank.TEN, Suit.HEARTS))
	caravan_2.add_base_card(create_numeric_card(Rank.FIVE, Suit.HEARTS))
	caravan_2.add_base_card(create_numeric_card(Rank.TEN, Suit.HEARTS))
	caravan_3.add_base_card(create_numeric_card(Rank.TEN, Suit.HEARTS))
	caravan_3.add_base_card(create_numeric_card(Rank.FIVE, Suit.HEARTS))
	caravan_3.add_base_card(create_numeric_card(Rank.TEN, Suit.HEARTS))

	game_result = apply_move(game_state, play_base_move)

	# Assert that player 1 won by 'selling' all 3 of their caravans
	assert game_result == GameResult(
		winner_id=player_to_play,
		reason=WinReason.THREE_CARAVANS,
		end_turn_number=turn_number
	)


def test_two_caravan_sales_victory():
	hand_card = create_numeric_card(Rank.EIGHT, Suit.HEARTS)
	hand_card_p2 = create_numeric_card(Rank.EIGHT, Suit.HEARTS)
	deck_card = create_numeric_card(Rank.FIVE, Suit.HEARTS)

	player_1 = create_player([deck_card], [hand_card])
	player_2 = create_player([], [hand_card_p2])

	caravans = initialise_caravans()

	caravan_to_play = CaravanId.P1_A
	player_to_play = PlayerId.P1
	turn_number = 19

	game_state = create_game_state(
		players=[player_1, player_2],
		caravans=caravans,
		current_player=player_to_play,
		game_phase=GamePhase.MAIN,
		turn_number=turn_number
	)

	play_base_move = create_move(
		PlayCard,
		player_id=player_to_play,
		card_id=hand_card.id,
		caravan_id=caravan_to_play,
	)
	caravan = game_state.get_caravan(caravan_to_play)
	caravan_2 = game_state.get_caravan(CaravanId.P1_B)
	caravan_3 = game_state.get_caravan(CaravanId.P2_C)

	caravan.add_base_card(create_numeric_card(Rank.EIGHT, Suit.HEARTS))
	caravan.add_base_card(create_numeric_card(Rank.FIVE, Suit.HEARTS))
	caravan_2.add_base_card(create_numeric_card(Rank.TEN, Suit.HEARTS))
	caravan_2.add_base_card(create_numeric_card(Rank.FIVE, Suit.HEARTS))
	caravan_2.add_base_card(create_numeric_card(Rank.TEN, Suit.HEARTS))
	caravan_3.add_base_card(create_numeric_card(Rank.TEN, Suit.HEARTS))
	caravan_3.add_base_card(create_numeric_card(Rank.FIVE, Suit.HEARTS))
	caravan_3.add_base_card(create_numeric_card(Rank.TEN, Suit.HEARTS))

	game_result = apply_move(game_state, play_base_move)

	# Assert that player 1 won by 'selling' 2 of their caravans whereas player 2 has locked the remaining route C
	assert game_result == GameResult(
		winner_id=player_to_play,
		reason=WinReason.TWO_CARAVANS,
		end_turn_number=turn_number
	)


def test_tied_caravan_sales():
	hand_card = create_numeric_card(Rank.EIGHT, Suit.HEARTS)
	hand_card_p2 = create_numeric_card(Rank.EIGHT, Suit.HEARTS)
	deck_card = create_numeric_card(Rank.FIVE, Suit.HEARTS)

	player_1 = create_player([deck_card], [hand_card])
	player_2 = create_player([], [hand_card_p2])

	caravans = initialise_caravans()

	caravan_to_play = CaravanId.P1_A
	player_to_play = PlayerId.P1
	turn_number = 19

	game_state = create_game_state(
		players=[player_1, player_2],
		caravans=caravans,
		current_player=player_to_play,
		game_phase=GamePhase.MAIN,
		turn_number=turn_number
	)

	play_base_move = create_move(
		PlayCard,
		player_id=player_to_play,
		card_id=hand_card.id,
		caravan_id=caravan_to_play,
	)
	caravan = game_state.get_caravan(caravan_to_play)
	caravan_2 = game_state.get_caravan(CaravanId.P1_B)
	caravan_3 = game_state.get_caravan(CaravanId.P1_C)
	caravan_4 = game_state.get_caravan(CaravanId.P2_C)

	caravan.add_base_card(create_numeric_card(Rank.EIGHT, Suit.HEARTS))
	caravan.add_base_card(create_numeric_card(Rank.FIVE, Suit.HEARTS))
	caravan_2.add_base_card(create_numeric_card(Rank.TEN, Suit.HEARTS))
	caravan_2.add_base_card(create_numeric_card(Rank.FIVE, Suit.HEARTS))
	caravan_2.add_base_card(create_numeric_card(Rank.TEN, Suit.HEARTS))
	caravan_3.add_base_card(create_numeric_card(Rank.TEN, Suit.HEARTS))
	caravan_3.add_base_card(create_numeric_card(Rank.FIVE, Suit.HEARTS))
	caravan_3.add_base_card(create_numeric_card(Rank.TEN, Suit.HEARTS))
	caravan_4.add_base_card(create_numeric_card(Rank.TEN, Suit.HEARTS))
	caravan_4.add_base_card(create_numeric_card(Rank.FIVE, Suit.HEARTS))
	caravan_4.add_base_card(create_numeric_card(Rank.TEN, Suit.HEARTS))

	game_result = apply_move(game_state, play_base_move)

	# Assert that the game is not finished even though player 1 has 'sold' all their caravans, as Route C is tied between the players
	assert game_result is None


def test_player_sells_caravan_but_loses():
	hand_card = create_numeric_card(Rank.ACE, Suit.HEARTS)
	hand_card_p2 = create_numeric_card(Rank.EIGHT, Suit.HEARTS)
	deck_card = create_numeric_card(Rank.FIVE, Suit.HEARTS)

	player_1 = create_player([deck_card], [hand_card])
	player_2 = create_player([], [hand_card_p2])

	caravans = initialise_caravans()

	caravan_to_play = CaravanId.P1_A
	player_to_play = PlayerId.P1
	turn_number = 19

	game_state = create_game_state(
		players=[player_1, player_2],
		caravans=caravans,
		current_player=player_to_play,
		game_phase=GamePhase.MAIN,
		turn_number=turn_number
	)

	play_base_move = create_move(
		PlayCard,
		player_id=player_to_play,
		card_id=hand_card.id,
		caravan_id=caravan_to_play,
	)
	caravan = game_state.get_caravan(caravan_to_play)
	caravan_2 = game_state.get_caravan(CaravanId.P2_A)
	caravan_3 = game_state.get_caravan(CaravanId.P2_B)
	caravan_4 = game_state.get_caravan(CaravanId.P2_C)

	caravan.add_base_card(create_numeric_card(Rank.TEN, Suit.HEARTS))
	caravan.add_base_card(create_numeric_card(Rank.FIVE, Suit.HEARTS))
	caravan.add_base_card(create_numeric_card(Rank.TEN, Suit.HEARTS))
	caravan_2.add_base_card(create_numeric_card(Rank.TEN, Suit.HEARTS))
	caravan_2.add_base_card(create_numeric_card(Rank.FIVE, Suit.HEARTS))
	caravan_2.add_base_card(create_numeric_card(Rank.TEN, Suit.HEARTS))
	caravan_3.add_base_card(create_numeric_card(Rank.TEN, Suit.HEARTS))
	caravan_3.add_base_card(create_numeric_card(Rank.FIVE, Suit.HEARTS))
	caravan_3.add_base_card(create_numeric_card(Rank.TEN, Suit.HEARTS))
	caravan_4.add_base_card(create_numeric_card(Rank.TEN, Suit.HEARTS))
	caravan_4.add_base_card(create_numeric_card(Rank.FIVE, Suit.HEARTS))
	caravan_4.add_base_card(create_numeric_card(Rank.TEN, Suit.HEARTS))

	game_result = apply_move(game_state, play_base_move)

	# Assert the situation where Player 1 selling Caravan A closes the final route and immediately loses them the game (Player 2 wins 2–1).
	assert game_result == GameResult(
		winner_id=PlayerId.P2,
		reason=WinReason.TWO_CARAVANS,
		end_turn_number=turn_number
	)

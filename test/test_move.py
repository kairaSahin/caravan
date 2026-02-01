from game.caravan.enums import CaravanId
from game.cards.enums import Rank, Suit
from game.engine.apply import apply_move
from game.moves.types import PlayCard
from game.player.enums import PlayerId
from game.state.enums import GamePhase
from test.functions import create_numeric_card, create_player, initialise_caravans, create_game_state, create_move


def test_play_base() -> None:
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

    # Assert that Player 1 holds the card in their hand
    assert hand_card.id in game_state.players[player_to_play].hand
    # Assert that Player 1 holds one card in their deck
    assert len(game_state.players[player_to_play].deck) == 1
    # Assert that Player 1's 1st caravan is empty
    assert len(game_state.get_caravan(caravan_to_play).pile) == 0

    apply_move(game_state, play_base_move)

    # Assert that the played card is no longer is in Player 1's hand
    assert hand_card.id not in game_state.players[player_to_play].hand

    # Assert that the played card has been successfully added to the caravan
    caravan = game_state.get_caravan(caravan_to_play)
    assert len(caravan.pile) == 1
    assert caravan.pile[-1].base_card.id == hand_card.id

    # Assert that Player 1 has drawn the next card in their deck to their hand and that their deck is now empty
    assert deck_card.id in game_state.players[player_to_play].hand
    assert len(game_state.players[player_to_play].deck) == 0

    # Assert that the turn has successfully progressed
    assert game_state.current_player == PlayerId.P2
    assert game_state.turn_number == 1


# TODO: Add multiple attach face card tests!
from game.engine.exceptions import IllegalMove
from game.moves.types import Move, PlayCard
from game.player.enums import PlayerId
from game.rules.ruleset import can_play_base
from game.state.enums import GamePhase
from game.state.functions import get_move_player
from game.state.game_state import GameState

def _draw_one_if_possible(state: GameState, move: Move) -> None:
    player = get_move_player(state, move)

    if not player.deck:
        # FIXME: If a player's deck is empty, they will lose. However this may be implemented somewhere else.
        return

    new_card = player.deck.pop()
    player.add_card_to_hand_card(new_card)

def _setup_complete_for_player(state: GameState, player_id: PlayerId) -> bool:
    # Should practically not occur as this should not be called if the game is not in setup mode
    # Added as failsafe.
    if state.game_phase != GamePhase.SETUP:
        return True

    for caravan_id, caravan in state.caravans.items():
        if caravan_id.owner == player_id and len(caravan.pile) == 0:
            return False

    return True

def _setup_complete_for_both(state: GameState) -> bool:
    return _setup_complete_for_player(state, PlayerId.P1) and _setup_complete_for_player(state, PlayerId.P2)

def _advance_after_play_base(state: GameState) -> None:
    if state.game_phase == GamePhase.SETUP:
        if _setup_complete_for_both(state):
            state.game_phase = GamePhase.MAIN

    state.turn_number += 1
    state.current_player = PlayerId.P2 if state.current_player == PlayerId.P1 else PlayerId.P1

def _apply_play_base(state: GameState, move: PlayCard) -> None:
    if not can_play_base(state, move):
        # TODO: Check raised errors later.
        raise IllegalMove("Play base move is not legal.")

    player = get_move_player(state, move)
    caravan = state.get_caravan(move.caravan_id)
    played_card = player.hand.pop(move.card_id)

    caravan.add_base_card(played_card)

    _draw_one_if_possible(state, move)
    _advance_after_play_base(state)

def apply_move(state: GameState, move: Move) -> None:
    if isinstance(move, PlayCard):
        _apply_play_base(state, move)
        return

    # TODO: Check raised errors later.
    raise IllegalMove(f"Unsupported move: {type(move).__name__}")
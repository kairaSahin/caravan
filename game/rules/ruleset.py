from game.caravan.enums import Direction
from game.cards.card import Card
from game.moves.types import MoveType, PlayCard, AttachFaceCard, DiscardCard, DiscardCaravan
from game.player.enums import PlayerId
from game.state.enums import GamePhase
from game.state.functions import get_move_player
from game.state.game_state import GameState

# TODO: May add explanation comments to go over the rules one by one for future clarity.
def _get_card_to_play(state: GameState, move: PlayCard | AttachFaceCard | DiscardCard) -> Card | None:
    player = get_move_player(state, move)

    if player is None:
        return None

    return player.hand.get(move.card_id)

def _is_players_turn(state: GameState, player_id: PlayerId) -> bool:
    return state.current_player == player_id

def _is_game_finished(state: GameState) -> bool:
    return state.game_phase == GamePhase.FINISHED

def _has_card_in_hand(state: GameState, move: PlayCard | AttachFaceCard | DiscardCard) -> bool:
    player = get_move_player(state, move)

    if player is None:
        return False

    return move.card_id in player.hand

def _is_card_numeric(state: GameState, move: PlayCard) -> bool:
    played_card = _get_card_to_play(state, move)

    if played_card is None:
        return False

    return played_card.rank.is_numeric

def _caravan_belongs_to_player(move: PlayCard | DiscardCaravan) -> bool:
    return move.caravan_id.owner == move.player_id

def _is_valid_setup(state: GameState, move: PlayCard) -> bool:
    if state.game_phase != GamePhase.SETUP:
        return True

    caravan = state.get_caravan(move.caravan_id)

    if caravan is None:
        return False

    return len(caravan.pile) == 0

def _caravan_direction_or_suit_is_valid(state: GameState, move: PlayCard) -> bool:
    caravan = state.get_caravan(move.caravan_id)
    played_card = _get_card_to_play(state, move)

    if played_card is None or caravan is None:
        return False

    top_card = caravan.top_card

    if top_card is None:
        return True

    top_value = top_card.base_card.base_value
    played_value = played_card.base_value

    if top_value == played_value:
        return False

    direction = caravan.direction

    if direction == Direction.UNSET:
        return True

    suit_valid = (caravan.current_suit is not None and caravan.current_suit == played_card.suit)
    direction_valid = ((top_value > played_value and direction == Direction.DESCENDING)
                        or
                       (top_value < played_value and direction == Direction.ASCENDING))

    return suit_valid or direction_valid

def can_play_base(state: GameState, move: PlayCard) -> bool:
    return (not _is_game_finished(state) and
            move.move_type is MoveType.PLAY_BASE and
            _is_players_turn(state, move.player_id) and
            _has_card_in_hand(state, move) and
            _is_card_numeric(state, move) and
            _caravan_belongs_to_player(move) and
            _is_valid_setup(state, move) and
            _caravan_direction_or_suit_is_valid(state, move)
    )

# TODO: Add other move rules.
from enum import Enum


class Rank(Enum):
    ACE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    TEN = 10

    KING = 'K'
    QUEEN = 'Q'
    JACK = 'J'
    JOKER = 'JK'

    _NUMERIC_RANKS = {
        ACE,
        TWO,
        THREE,
        FOUR,
        FIVE,
        SIX,
        SEVEN,
        EIGHT,
        NINE,
        TEN,
    }

    @property
    def is_numeric(self) -> bool:
        return self in Rank._NUMERIC_RANKS


class _Suit(Enum):
    HEARTS = 'H'
    DIAMONDS = 'D'
    CLUBS = 'C'
    SPADES = 'S'

# TODO: This may unnecessarily complicate functions in the future, by always requiring 'None' validations.
type Suit = _Suit | None
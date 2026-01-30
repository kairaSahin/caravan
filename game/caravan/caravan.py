from dataclasses import dataclass, field
from uuid import UUID

from game.caravan.enums import Direction, CaravanId
from game.cards.card import Card, PlayedCard
from game.cards.enums import Suit, Rank


@dataclass
class Caravan:
    id: CaravanId
    pile: list[PlayedCard] = field(default_factory=list)

    @property
    def top_card(self) -> PlayedCard | None:
        return self.pile[-1] if len(self.pile) > 0 else None

    @property
    def direction(self) -> Direction:
        # If a caravan has no or just one card, there is no direction, return no direction;
        if len(self.pile) < 2:
            return Direction.UNSET

        ultimate_card = self.top_card

        if ultimate_card is None:
            return Direction.UNSET

        ultimate_card_value = ultimate_card.base_card.base_value
        penultimate_card_value = self.pile[-2].base_card.base_value

        # This case is practically not possible.
        # Playing a card on another card with the same rank is invalid per game rules.
        if ultimate_card_value == penultimate_card_value:
            return Direction.UNSET

        # If the last card is higher than the previous one, the caravan is ascending; if it's lower, then the caravan is descending.
        base_direction = Direction.ASCENDING if ultimate_card_value > penultimate_card_value else Direction.DESCENDING

        if ultimate_card.queen_count % 2 == 1:
            return Direction.ASCENDING if base_direction == Direction.DESCENDING else Direction.DESCENDING

        return base_direction


    @property
    def current_suit(self) -> Suit | None:
        if not self.pile:
            return None

        ultimate_card = self.top_card

        return ultimate_card.last_queen_suit or ultimate_card.base_card.suit

    @property
    def score(self) -> int:
        score = 0

        for card in self.pile:
            card_value = card.base_card.base_value
            kings = sum(1 for face_card in card.attachments if face_card.rank == Rank.KING)
            # Score of a numeric card is multiplied by 2 for each King attached.
            # Ex: 3 with 2 Kings -> 3 * 2 * 2 = 12.
            score += card_value * (2 ** kings)

        return score

    # TODO: Check if methods 'add_base_card', 'attach' should return bool for success.
    def add_base_card(self, card: Card) -> None:
        if not card.rank.is_numeric:
            # TODO: Check raised errors later.
            raise ValueError("Base cards in caravan must be ACE–TEN.")

        self.pile.append(PlayedCard(base_card=card))

    # TODO: Check id usage.
    def attach(self, target_card_id: UUID, face_card: Card) -> None:
        if face_card.rank.is_numeric:
            # TODO: Check raised errors later.
            raise ValueError("Face cards in caravan must be JACK-KING or JOKER.")

        for played_card in self.pile:
            if played_card.base_card.id == target_card_id:
                played_card.attachments.append(face_card)
                return

        # TODO: Check raised errors later.
        raise KeyError(f"Target card id {target_card_id} not found in pile")

    def remove_base_card(self, target_base_id: UUID) -> None:
        self.pile = [played_card for played_card in self.pile if played_card.base_card.id != target_base_id]

    def discard_caravan(self) -> None:
        self.pile.clear()
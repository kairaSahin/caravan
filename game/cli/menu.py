from uuid import UUID

from game.caravan.enums import CaravanId
from game.moves.types import PlayCard, Move, AttachFaceCard, DiscardCard, DiscardCaravan, Concede
from game.state.game_state import GameState
from game.cli.printer import print_player_hand_and_deck_count, print_routes, print_caravan_pile_with_indices


def _ask_int(min_input: int, max_input: int) -> int | None:
	while True:
		try:
			choice = int(input("> "))
		except ValueError:
			print("Enter a number.")
			continue

		if min_input <= choice <= max_input:
			return choice

		print("Choose within input range.")


def _choose_card_from_hand(state: GameState) -> UUID:
	current_player = state.players.get(state.current_player)

	print("Choose card:")
	print_player_hand_and_deck_count(current_player)

	player_hand = list(current_player.hand.values())

	card_choice = _ask_int(0, len(player_hand) - 1)
	card = player_hand[card_choice]

	return card.id


def _choose_caravan(state: GameState, any_caravan=False) -> CaravanId:
	if any_caravan:
		caravan_id_options = list(CaravanId)
	else:
		caravan_id_options = [cid for cid in CaravanId if cid.owner == state.current_player]

	print_routes(state, True)

	print("Choose caravan:")
	for i, caravan_id in enumerate(caravan_id_options):
		print(f"\t[{i}]: {caravan_id}")

	index = _ask_int(0, len(caravan_id_options) - 1)

	return caravan_id_options[index]


def _choose_target_base_card_from_caravan(state: GameState, caravan_id: CaravanId) -> UUID:
	caravan = state.get_caravan(caravan_id)

	if caravan is None:
		raise ValueError("Invalid caravan.")
	if not caravan.pile:
		raise ValueError("Cannot attach to an empty caravan.")

	print_caravan_pile_with_indices(state, caravan_id)

	index = _ask_int(0, len(caravan.pile) - 1)

	return caravan.pile[index].base_card.id


def choose_action_menu(state: GameState) -> Move:
	print("Choose action:")
	print("\t[0]: Play base card")
	print("\t[1]: Play face card")
	print("\t[2]: Discard card")
	print("\t[3]: Discard caravan")
	print("\t[4]: Concede")

	choice = _ask_int(0, 4)
	current_player = state.current_player

	if choice == 0:
		card_id = _choose_card_from_hand(state)
		caravan_id = _choose_caravan(state)
		return PlayCard(player_id=current_player, card_id=card_id, caravan_id=caravan_id)

	elif choice == 1:
		card_id = _choose_card_from_hand(state)
		caravan_id = _choose_caravan(state, any_caravan=True)
		target_card_id = _choose_target_base_card_from_caravan(state, caravan_id)
		return AttachFaceCard(player_id=current_player, card_id=card_id, caravan_id=caravan_id,
							  target_base_id=target_card_id)
	elif choice == 2:
		card_id = _choose_card_from_hand(state)
		return DiscardCard(player_id=current_player, card_id=card_id)
	elif choice == 3:
		caravan_id = _choose_caravan(state)
		return DiscardCaravan(player_id=current_player, caravan_id=caravan_id)
	else:
		return Concede(player_id=current_player)

from game.caravan.caravan import Caravan
from game.caravan.enums import CaravanId
from game.cards.card import Card
from game.player.enums import PlayerId
from game.setup.game_config import GameConfig
from game.state.enums import GamePhase
from game.state.game_state import GameState, PlayerState


def init_game(game_config: GameConfig) -> GameState:
	players = initialize_players(game_config)

	game_state = GameState(
		players=players,
		caravans=initialize_caravans(),
		current_player=game_config.starting_player,
		turn_number=0,
		game_phase=GamePhase.SETUP,
		game_result=None
	)

	deal_for_setup(game_state, game_config.starting_hand_size)

	return game_state


def create_player_state(deck: list[Card]) -> PlayerState:
	return PlayerState(deck=deck, hand={})


def initialize_players(game_config: GameConfig) -> dict[PlayerId, PlayerState]:
	players = {}

	for player_id in PlayerId:
		deck = game_config.deck_builder(player_id)

		if game_config.shuffle_decks:
			game_config.random_generator.shuffle(deck)

		player_state = create_player_state(deck)
		players[player_id] = player_state

	return players


def deal_for_setup(state: GameState, starting_hand_size: int) -> None:
	for player_id, player in state.players.items():
		if len(player.deck) < starting_hand_size:
			raise ValueError(
				f"Deck ({len(player.deck)}) too small to deal {starting_hand_size} for player P{player_id}.")

		for _ in range(starting_hand_size):
			card = player.deck.pop()

			player.hand[card.id] = card


def initialize_caravans() -> dict[CaravanId, Caravan]:
	return {caravan_id: Caravan(id=caravan_id) for caravan_id in CaravanId}

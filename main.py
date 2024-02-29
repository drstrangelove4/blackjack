import pyinputplus as pyip
from deck import Deck
from player import Player

# ----------------------------------------------------------------------------------------------------------------------
# Constants

DEALER = 1
BLACKJACK = 21
DEALER_STOP_SCORE = 17
BLACKJACK_MULTIPLIER = 2.25
WINNING_MULTIPLIER = 2
STARTING_BET = 0
NO_CHIPS = 0
INVALID = 1
FIRST_CARD = 0
DEALER_INDEX = 0
STARTING_CARDS = 2


# ----------------------------------------------------------------------------------------------------------------------
def dealer_actions(dealer, deck):
    """
    Responsible for the dealers actions. Draws cards until they have a score of 17 or greater.
    """
    hitting = True
    while hitting:
        dealer.show_cards()

        # If the dealer has a score of 17 or more terminate its actions.
        if dealer.get_score() >= DEALER_STOP_SCORE:
            # Check if dealer has bust, 21 or blackjack.
            status = dealer.get_status()
            if status:
                print(status)
            break
        else:
            dealer.draw_card(deck.deal_card())


# ----------------------------------------------------------------------------------------------------------------------


def draw_cards(player_list, dealer, deck):
    """
    Draws cards and checks game status.  If score is over or equal to 21 end the turn.
    """

    for player in player_list:
        # In blackjack the dealer only shows 1 card - the other is hidden.
        print(
            f"\nDealer is showing a {dealer.cards[FIRST_CARD].name} for a score of {dealer.cards[FIRST_CARD].value}\n"
            f"-----------------------------------------------------------------------------------"
        )

        hitting = True
        while hitting:
            # display cards to user
            player.show_cards()

            # Checks to see if player score is 21 or greater than 21. This will terminate the players turn.
            if player.get_score() >= BLACKJACK:
                status = player.get_status()
                print(status)
                break

            # option to draw cards and input checking
            print("Draw a card (yes/no)?:")
            choice = pyip.inputYesNo().lower()

            # If player doesn't take draw option, terminate their turn, else continue drawing.
            if choice == "y" or choice == "yes":
                player.draw_card(deck.deal_card())
            else:
                break


# ----------------------------------------------------------------------------------------------------------------------


def add_players(is_dealer):
    """
    Creates player objects, a list of players
    """

    player_list = []

    # Takes input if we are adding humans. If we are adding a dealer use a default value.
    if not is_dealer:
        print("How many players?:")
        number_of_players = pyip.inputNum()
    else:
        number_of_players = DEALER

    # Get the name of the player and create the player object with 2 card objects assigned to them.
    for x in range(number_of_players):
        # Takes name input from players, else we are adding a dealer.
        if not is_dealer:
            print(f"What is the name of player {x + 1}")
            player_name = pyip.inputStr()
        else:
            player_name = "Dealer"

        # Save the player object (which contains their initial cards) to a list which the function will return.
        player = Player(name=player_name)
        player_list.append(player)

    return player_list


# ----------------------------------------------------------------------------------------------------------------------


def take_bets(players_list):
    """
    Loops through players and takes bets. Calls the function that deducts chips and stores bet amounts.
    """

    for player in players_list:
        # Take bets from players
        betting = True
        while betting:

            # Asks for and takes a bet - ensures it is a number value.
            print(f"{player.name} you have {player.chips}. Make a bet:")
            bet = pyip.inputNum()

            # Check if the bet was valid
            return_code = player.make_bet(bet_amount=bet)

            # Keep asking for input unless we get a valid amount
            if return_code == INVALID:
                print("Invalid bet amount!")
            else:
                betting = False


# ----------------------------------------------------------------------------------------------------------------------


def hand_assessment(player_list, dealer):
    """
    Takes the players holdings and dealers holdings and compares them. Assigns winnings/losses based upon the ruleset of
    blackjack.
    """
    # Dealer blackjack game state
    if dealer.has_blackjack:
        dealer.blackjack()
        for player in player_list:
            if player.has_blackjack:
                player.blackjack()
                player.add_winnings(player.current_bet)
            else:
                player.lose_bet()

    else:
        for player in player_list:
            # Player blackjack state
            winnings = NO_CHIPS
            if player.has_blackjack:
                player.blackjack()
                winnings = player.current_bet * BLACKJACK_MULTIPLIER

            # Other conditions
            else:
                # Player beats dealer
                if player.score > dealer.score and not player.has_bust or dealer.has_bust and not player.has_bust:
                    winnings = player.current_bet * WINNING_MULTIPLIER
                # Dealer equals player
                elif player.score == dealer.score and not player.has_bust:
                    winnings = player.current_bet

            compare_score(player, dealer)

            # If there are winnings, add them to player total.
            if winnings != NO_CHIPS:
                player.add_winnings(winnings)
            else:
                player.lose_bet()

            player.current_bet = STARTING_BET


# ----------------------------------------------------------------------------------------------------------------------


def compare_score(player, dealer):
    """
    Prints the dealer score and the player score to the terminal.
    """
    print(f"{dealer.name} has {dealer.score}, {player.name} has {player.score}")


# ----------------------------------------------------------------------------------------------------------------------

def player_management(player_list):
    """
    Allows the user to add chips or remove players who are bust (although they can continue with 0 chips for fun).
    """

    for player in player_list:
        # Give the option to add chips to players with 0 chips.
        if player.chips == NO_CHIPS:
            print(f"{player.name}, would you like to add chips?")
            choice = pyip.inputYesNo()
            if choice.lower() == "yes":
                print("How many chips would you like to add?: ")
                amount = pyip.inputNum()
                player.chips += amount

            # Option to remove players with 0 chips.
            else:
                print(f"Would you like to remove {player.name} from the game?")
                choice = pyip.inputYesNo()
                if choice.lower() == "yes":
                    del player_list[player_list.index(player)]
                else:
                    print(f"{player.name} is continuing with no chips.")


# ----------------------------------------------------------------------------------------------------------------------

def deal_cards(players_list, deck):
    """
    Assigns starting cards to every player provided in a list.
    """
    for player in players_list:
        for x in range(STARTING_CARDS):
            player.add_card(deck.deal_card())


# ----------------------------------------------------------------------------------------------------------------------

def clear_cards(player_list):
    """
    For each player passed to the function in a list, calls the function used to remove player cards assigned to a
    player.
    """
    for player in player_list:
        player.remove_cards()


# ----------------------------------------------------------------------------------------------------------------------

def main():
    """
    Main function. Controls the game state and order. Holds player objects.
    """

    # Add players to the game
    players = add_players(is_dealer=False)
    # Create a dealer
    dealer = add_players(is_dealer=True)

    playing = True
    while playing:
        # Create a deck object
        deck = Deck()

        # Add chips or give the option to remove bust players.
        player_management(player_list=players)

        # deal initial cards to players and dealer
        deal_cards(players_list=players, deck=deck)
        deal_cards(players_list=dealer, deck=deck)

        # Take user bets
        take_bets(players_list=players)

        # User actions
        draw_cards(player_list=players, dealer=dealer[DEALER_INDEX], deck=deck)

        # Dealer Actions
        dealer_actions(dealer=dealer[DEALER_INDEX], deck=deck)

        # Looks at player hands and assigns chip winnings(if any).
        hand_assessment(player_list=players, dealer=dealer[DEALER_INDEX])

        # Logic for allowing the game to continue/stop after round.
        print("\nWould you like to play another round?:")
        choice = pyip.inputYesNo()
        print(choice)
        if choice.lower() != "yes":
            print("Game over!")
            playing = False
        else:
            clear_cards(player_list=players)
            clear_cards(player_list=dealer)

    # TODO:
    # Add functionality to allow ace to be 1 or 11.


if __name__ == "__main__":
    main()

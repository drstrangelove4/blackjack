BLACKJACK = 21
MAX_BLACKJACK_CARDS = 2
ERROR = 1
SUCCESS = 0
STARTING_SCORE = 0
STARTING_BET = 0
STARTING_CHIPS = 100


class Player:
    """
    Player object that holds card objects taken from the deck object.
    """

    def __init__(self, name):
        self.name = name
        self.cards = []
        self.chips = STARTING_CHIPS
        self.current_bet = STARTING_BET
        self.score = STARTING_SCORE
        self.has_bust = False
        self.has_blackjack = False

    # ------------------------------------------------------------------------------------------------------------------

    def make_bet(self, bet_amount):
        """
        Takes a bet amount and deducts it from the player object.
        Tracks current bet amount.
        """
        # Checks if the bet amount is valid. If not return a fail code.
        if self.chips - bet_amount < 0 or self.chips - bet_amount > self.chips:
            return ERROR

        # Reduce player chips and increase the bet amount upon successful input. Return a success code.
        else:
            self.current_bet += bet_amount
            self.chips -= bet_amount
            return SUCCESS

    # ------------------------------------------------------------------------------------------------------------------

    def draw_card(self, card):
        """
        Adds a card to the player list
        """

        self.cards.append(card)

    # ------------------------------------------------------------------------------------------------------------------

    def show_cards(self):
        """
        Prints the cards + score the player currently has
        """
        # Displays the cards assigned to the player object.
        print(f"\n{self.name}'s cards\n--------------------")
        for card in self.cards:
            print(card.name, end=" ")

        # Displays the current score of player object cards.
        current_score = self.get_score()
        print(f"\nScore is: {current_score}\n")

    # ------------------------------------------------------------------------------------------------------------------

    def get_score(self):
        """
        Adds the total value of the players cards
        """
        # Sets the score to 0 to prevent double counting on every call.
        self.score = STARTING_SCORE

        # Sums the score of the cards using card.value attributes.
        for card in self.cards:
            self.score += card.value

        # Changes bust attribute from false to true.
        if self.score > BLACKJACK:
            self.has_bust = True

        # Return score information to caller.
        return self.score

    # ------------------------------------------------------------------------------------------------------------------

    def get_status(self):
        """
        Takes the score and returns the status based upon the rules of blackjack.
        """
        # Return blackjack.
        if self.score == BLACKJACK and len(self.cards) == MAX_BLACKJACK_CARDS:
            self.has_blackjack = True
            return f"{self.name} has Blackjack!"

        # Return best possible, non blackjack score.
        elif self.score == BLACKJACK:
            return f"{self.name} has 21!"

        # Return bust.
        elif self.score > BLACKJACK:
            self.score = STARTING_SCORE
            return f"{self.name} has bust!"

    # ------------------------------------------------------------------------------------------------------------------

    def add_winnings(self, winnings_amount):
        self.chips += winnings_amount
        print(f"{self.name} has won {winnings_amount} chips! {self.name} now has {self.chips} chips")

    # ------------------------------------------------------------------------------------------------------------------

    def lose_bet(self):
        print(f"{self.name} has lost {self.current_bet} and now has {self.chips} remaining.")

    # ------------------------------------------------------------------------------------------------------------------

    def blackjack(self):
        if self.has_blackjack:
            print(f"{self.name} has BLACKJACK")

    # ------------------------------------------------------------------------------------------------------------------

    def remove_cards(self):
        self.cards = []

    # ------------------------------------------------------------------------------------------------------------------

    def add_card(self, card):
        self.cards.append(card)

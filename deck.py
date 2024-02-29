import random

SUITS = 4


class Card:
    """
    Card object that takes 2 arguments - a name and a value. Used for creating individual elements of a deck object.
    """

    def __init__(self, name, value):
        self.name = name
        self.value = value

    # ------------------------------------------------------------------------------------------------------------------


class Deck:
    """
    Deck object. Made up of 52 card objects which are stored in a list (self.cards)
    """

    def __init__(self):

        # Names of the cards found in a standard deck.
        card_names = [
            "Ace",
            "King",
            "Queen",
            "Jack",
            "10",
            "9",
            "8",
            "7",
            "6",
            "5",
            "4",
            "3",
            "2",
        ]

        # Numerical values assigned to each card - needed to calculate scores.
        card_values = [11, 10, 10, 10, 10, 9, 8, 7, 6, 5, 4, 3, 2]

        # Holds the deck of cards.
        self.cards = []

        # Create the deck on initialization and randomize the order.
        self.populate_deck(card_names=card_names, card_values=card_values)
        self.shuffle_deck()

    # ------------------------------------------------------------------------------------------------------------------

    def populate_deck(self, card_names, card_values):
        """
        Build a deck from card objects
        """
        # Iterate over the above lists 4 times, creating a card object for each, to create a standard deck object.
        for _ in range(SUITS):
            for x in range(len(card_names)):
                new_card = Card(name=card_names[x], value=card_values[x])
                # Adds cards to the deck.
                self.cards.append(new_card)

    # ------------------------------------------------------------------------------------------------------------------

    def shuffle_deck(self):
        """
        Give the deck a 'random' order.
        """

        random.shuffle(self.cards)

    # ------------------------------------------------------------------------------------------------------------------

    def deal_card(self):
        """
        Returns and removes from the deck, the first card of a randomized deck.
        """
        # Using pop instead of picking a random card and removing it simulates how a dealer would take a card from
        # the deck in real life.
        return self.cards.pop()

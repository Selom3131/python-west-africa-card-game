class Card:
    def __init__(self, rank = 2, suit = 'A'):
        self.rank = rank
        self.suit = suit

    def set_suit(self, suit):
        self.suit = suit

    def set_rank(self, rank):
        self.rank = rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def display(self):
        print(f'{self.suit}#{self.rank}')

    def __str__(self):
        return f'Suit : {self.suit} # Rank : {self.rank}'

    def __repr__(self):
        return str(self)

    def card_to_string(self):
        card = (
            '┌─────────┐\n'
            '│{}       │\n'
            '│         │\n'
            '│         │\n'
            '│    {}   │\n'
            '│         │\n'
            '│         │\n'
            '│       {}│\n'
            '└─────────┘\n'
        ).format(
            format(self.rank, ' <2'),
            format(self.suit, ' <2'),
            format(self.rank, ' >2')
        )
        print(card)


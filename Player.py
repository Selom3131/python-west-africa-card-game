class Player:
    def __init__(self, name, hand):
        self.hand = hand
        self.name = name

    def set_hand(self, hand):
        self.hand = hand

    def get_hand(self):
        return self.hand

    def set_name(self, name):
        self.name = name

    def get_name(self):
        return self.name

    def add_card_to_hand(self, card):

        self.hand.append(card)

    def __str__(self):
        return f'Player : {self.name} # Hand {self.hand}'

    def __repr__(self):
        return str(self)

    def display_player_hand(self):
        for card in self.hand:
            card.card_to_string()
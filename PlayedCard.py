from Card import Card


class PlayedCard(Card):
    def __init__(self, rank=2, suit='', players_name=''):
        Card.__init__(self, rank, suit)
        self.players_name = players_name

    def set_players_name(self, players_name):
        self.players_name = players_name

    def get_players_name(self):
        return self.players_name

    def __str__(self):
        return f"Player's name : {self.players_name} Suit : {self.suit} # Rank : {self.rank}"

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 31 11:02:54 2021

@author: ksa
West African SIPA Card Game Implementation
"""

import requests
import random
from Card import Card
from Player import Player
from PlayedCard import PlayedCard

DECK = []
CARD_SUIT_SYMBOLS = ['♠', '♦', '♥', '♣']
MASTERS = ['A', 'K', 'Q', 'J']

CARD_RANKING = {'2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9,'10':10, 'J':11, 'Q':12, 'K':13,'A':14}

GAME_HISTORY = []
TOP_CARD = PlayedCard()
SPECIAL_MESSAGE = ''


def get_bigger_or_equivalent(first_card: PlayedCard, second_card: PlayedCard) -> {'status': str, 'card': PlayedCard}:
    result = {'status': 'unbeaten', 'card': first_card}
    if first_card.suit == second_card.suit:
        if CARD_RANKING[second_card.rank] > CARD_RANKING[first_card.rank]:
            return {'status': 'beaten', 'card': second_card}
        else:
            return result
    else:
        if CARD_RANKING[second_card.rank] == CARD_RANKING[first_card.rank]:

            return {'status': 'shifted', 'card': second_card}

        return result


def ascii_version_of_card(*cards, return_string=True):
    """
    Instead of a boring text version of the card we render an ASCII image of the card.
    :param cards: One or more card objects
    :param return_string: By default we return the string version of the card, but the dealer hide the 1st card and we
    keep it as a list so that the dealer can add a hidden card in front of the list
    """
    # we will use this to prints the appropriate icons for each card
    suits_name = ['Spades', 'Diamonds', 'Hearts', 'Clubs']
    suits_symbols = ['♠', '♦', '♥', '♣']

    # create an empty list of list, each sublist is a line
    lines = [[] for i in range(9)]

    for index, card in enumerate(cards[0]):
        # value = card[0]
        # print(type(card))
        # print(len(card))
        # print(value)

        # "King" should be "K" and "10" should still be "10"
        if card.rank == '10':  # ten is the only one who's rank is 2 char long
            space = ''  # if we write "10" on the card that line will be 1 char to long
        else:
            space = ' '  # no "10", we use a blank space to will the void
        # get the cards suit
        rank = card.rank
        suit = card.suit

        # add the individual card on a line by line basis

        lines[0].append('┌─────────┐')
        lines[1].append('│{}{}       │'.format(rank, space))  # use two {} one for char, one for space or char
        lines[2].append('│         │')
        lines[3].append('│         │')
        lines[4].append('│    {}    │'.format(suit))
        lines[5].append('│         │')
        lines[6].append('│         │')
        lines[7].append('│       {}{}│'.format(space, rank))
        lines[8].append('└─────────┘')

    result = []
    for index, line in enumerate(lines):
        result.append(''.join(lines[index]))

    # hidden cards do not use string
    if return_string:
        return '\n'.join(result)
    else:
        return result


def load_deck():
    for symbol in CARD_SUIT_SYMBOLS:
        for card_type in MASTERS:
            card = Card(card_type, symbol)
            DECK.append(card)
        for card_num in range(2, 11):
            card = Card(str(card_num), symbol)
            DECK.append(card)


def display_deck():

    print(DECK)


def collect_list_of_player():
    is_list_completed = False
    list_of_players = []
    # number_of_players = int(input("""
    # How many players are going to participate?
    # Nota Bene : This game requires a minimum of 2 players
    # """))

    for i in range(1, 3):
        name_player = input(f"""
        Please enter the player No {i} name : """)
        player = Player(name_player, [])
        list_of_players.append(player)

    return list_of_players





def display_help():
    return input(f"""
    This is guide for the game""")


def play_game(list_of_player):
    process_game = {"quit": False, "turn": 0}
    # turn = 0
    while not process_game["quit"] and (len(list_of_player[0].hand) > 0 or len(list_of_player[1].hand) > 0):
        print(f'Turn {process_game["turn"]}')
        print(f'{list_of_player[0].get_name()} Size # {len(list_of_player[0].hand)}')
        print(f'{list_of_player[1].get_name()} Size # {len(list_of_player[1].hand)}')
        if process_game["turn"] % 2 == 0:

            process_game = process_player(list_of_player[0], process_game["turn"])

        else:

            process_game = process_player(list_of_player[1], process_game["turn"])

        # turn += 1

    print(f'{TOP_CARD.get_players_name()} is the Winner !!!. \nCongrats {TOP_CARD.get_players_name()}!')


def process_player(player: Player, turn):
    global TOP_CARD
    global SPECIAL_MESSAGE
    process_game = {"quit": False, "turn": turn}

    # quit_game = False
    hand = player.hand
    option = [""]
    print(ascii_version_of_card(hand))
    while option[0] not in ["-dc", "--help", "--quit"]:

        option = input(f"""

 {SPECIAL_MESSAGE}
It's {player.name}'s turn.
Type :
-d: to  display your hand
-dc [card number counting from left to right]: drop your card
--quit
--help
                """).split(" ")

        if option[0] == "-d":
            print(ascii_version_of_card(hand))
        elif option[0] == "-dc":

            # check if the card selected by the current player is within available cards range
            # display the menu to the player again
            if int(option[1]) not in range(len(hand)):
                SPECIAL_MESSAGE = f"""SPECIAL MESSAGE !!!
                {player.get_name()}, the card number selected in should be within a range of 1 to {len(hand)}"""

                continue

            dropped_card: Card = hand[int(option[1]) - 1]

            # Add the dropped card to the History
            GAME_HISTORY.append(dropped_card)

            # Check get the biggest value's card 
            if TOP_CARD.get_players_name() == "" or TOP_CARD.get_players_name() == player.get_name():

                TOP_CARD = PlayedCard(dropped_card.get_rank(), dropped_card.get_suit(), player.name)
                process_game["turn"] += 1
            else:  # The current player's is not the one who played the card on top
                # fetch the current card on top of the game
                current_top_played_card = PlayedCard(TOP_CARD.get_rank(), TOP_CARD.get_suit(), TOP_CARD.get_players_name())
                # fetch the dropped card to be compared to the current card
                dropped_played_card = PlayedCard(dropped_card.get_rank(), dropped_card.get_suit(), player.get_name())
                # compare the two card to determine whether the current card is beaten
                compare_result = get_bigger_or_equivalent(current_top_played_card, dropped_played_card)
                print(f'Comparison result : {compare_result}')
                bigger_card = compare_result['card']
                TOP_CARD = PlayedCard(bigger_card.get_rank(), bigger_card.get_suit(), bigger_card.get_players_name())

                if current_top_played_card.get_players_name() != TOP_CARD.get_players_name():
                    # the current player has beaten the other player's top card
                    if compare_result['status'] != 'beaten':
                        process_game["turn"] += 1
                else:
                    process_game["turn"] += 1
            # Increment the turn for next player to proceed.


            print(TOP_CARD)
            hand.pop(int(option[1]) - 1)
            print(ascii_version_of_card(GAME_HISTORY))
        elif option[0] == "--help":
            display_help()
        elif option[0] == "--quit":
            process_game["quit"] = True

    return process_game


load_deck()

random.shuffle(DECK)

players = collect_list_of_player()
print(len(DECK))
# Dispatch 5 cards from the top of the deck to each of the two players
for i in range(14):
    if i % 2 == 0:  # pick a card for player number 1

        players[0].add_card_to_hand(DECK[-1])
        DECK.pop(-1)
    else:  # pick a card for player number 2

        players[1].add_card_to_hand(DECK[-1])
        DECK.pop(-1)

play_game(players)


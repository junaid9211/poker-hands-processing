import re

NUMERICAL_VALUE = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, 'T': 10, 'J': 11, 'Q': 12,
                   'K': 13, 'A': 14}


class Board:
    """
    Board class represents a board of 3 cards
    """

    def __init__(self, board_str: str):
        self.board_str = board_str
        self.cards = re.findall(r'[23456789TJQKA]', board_str)
        self.suits = re.findall(r'[shdc]', board_str)
        self.values = [NUMERICAL_VALUE[card] for card in self.cards]

        self.cards_info = [{'card': card, 'suit': suit, 'value': value}
                           for card, suit, value in
                           zip(self.cards, self.suits, self.values)]

        self.cards_info = sorted(self.cards_info, key=lambda d: d['value'], reverse=True)

        self.cards = [card['card'] for card in self.cards_info]
        self.suits = [card['suit'] for card in self.cards_info]
        self.values = [card['value'] for card in self.cards_info]

        self.first = self.cards[0]
        self.second = self.cards[1]
        self.third = self.cards[2]



class Hand:
    """
    Hand class represents a hand of 2 cards
    This class is exact copy and paste of board except it does not have a self.third card property
    """

    def __init__(self, hand_str: str):
        self.hand_str = hand_str
        self.cards = re.findall(r'[23456789TJQKA]', hand_str)
        self.suits = re.findall(r'[shdc]', hand_str)
        self.values = [NUMERICAL_VALUE[card] for card in self.cards]

        self.cards_info = [{'card': card, 'suit': suit, 'value': value}
                           for card, suit, value in
                           zip(self.cards, self.suits, self.values)]

        self.cards_info = sorted(self.cards_info, key=lambda d: d['value'], reverse=True)

        self.cards = [card['card'] for card in self.cards_info]
        self.suits = [card['suit'] for card in self.cards_info]
        self.values = [card['value'] for card in self.cards_info]

        self.first = self.cards[0]
        self.second = self.cards[1]


class Category:
    @staticmethod
    def is_HaveTopPair(board: Board, hand: Hand) -> bool:
        return board.first in hand.cards

    @staticmethod
    def is_HaveSecondTopPair(board: Board, hand: Hand) -> bool:
        return board.second in hand.cards

    @staticmethod
    def is_HaveThirdTopPair(board: Board, hand: Hand) -> bool:
        return board.third in hand.cards

    @staticmethod
    def is_HaveTopTwoPair(board: Board, hand: Hand) -> bool:
        return board.first in hand.cards and board.second in hand.cards

    @staticmethod
    def is_HaveBottomTwoPair(board: Board, hand: Hand) -> bool:
        return board.second in hand.cards and board.third in hand.cards

    @staticmethod
    def is_HaveTwoPair(board: Board, hand: Hand) -> bool:
        return board.first in hand.cards and board.third in hand.cards

    @staticmethod
    def is_HaveTopSet(board: Board, hand: Hand) -> bool:
        if hand.first == hand.second:
            return hand.first == board.first
        else:
            return False

    @staticmethod
    def is_HaveSet(board: Board, hand: Hand) -> bool:
        if hand.first == hand.second:
            return hand.first == board.second or hand.first == board.third
        else:
            return False

    @staticmethod
    def is_HaveTrips(board: Board, hand: Hand) -> bool:
        trips = False
        for card in board.cards:
            if board.cards.count(card) == 2 and card in hand.cards:
                trips = True
                break

        return trips

    @staticmethod
    def is_HaveQuads(board: Board, hand: Hand) -> bool:
        all_cards = board.cards + hand.cards
        unique_cards = set(all_cards)
        return len(unique_cards) == 2

    @staticmethod
    def is_HaveFlush(board: Board, hand: Hand) -> bool:
        all_suits = board.suits + hand.suits
        unique_suits = set(all_suits)
        return len(unique_suits) == 1

    @staticmethod
    def is_HaveStraight(board: Board, hand: Hand) -> bool:
        all_cards = board.cards + hand.cards

        # value of A is 1 if there is 2 in cards else it is 14
        value_of_ace = 1 if '2' in all_cards else 14
        numerical_value = {'T': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': value_of_ace}

        straight = True
        card_nums = [int(card) if card.isdigit() else numerical_value[card] for card in all_cards]

        card_nums.sort()

        # assuming my code is correct, what if A is supposed to be 1?
        for i in range(len(card_nums) - 1):
            if card_nums[i] + 1 != card_nums[i + 1]:
                straight = False
                break

        return straight

    @staticmethod
    def is_HaveOverPair(board: Board, hand: Hand) -> bool:
        board_max_value = board.cards_info[0]['value']
        return board_max_value > hand.values[0] and board_max_value > hand.values[1]


    @staticmethod
    def is_HaveFullHouse(board: Board, hand: Hand) -> bool:
        # three of same cards and two of same cards
        all_cards = board.cards + hand.cards
        unique_cards = list(set(all_cards))

        if len(unique_cards) == 2:
            return (all_cards.count(unique_cards[0]) == 3 and all_cards.count(unique_cards[1]) == 2 or
                    all_cards.count(unique_cards[1]) == 3 and all_cards.count(unique_cards[0]) == 2)
        else:
            return False


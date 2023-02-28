import re

NUMERICAL_VALUE = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, 'T': 10, 'J': 11, 'Q': 12,
                   'K': 13, 'A': 14}

KEY_NAMES = ['Bet', 'Check', 'Raise', 'Call', 'Fold']


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


class Output:
    """Represents one instance of output: output of one rstring"""

    def __init__(self, player_num, preflop, pattern, filename, hands_info):
        self.player_num = player_num
        self.preflop = preflop
        self.pattern = pattern
        self.filename = filename
        self.hands_info = hands_info

    # TODO gives output in string format
    def get_output(self):
        output_str = ''

        for key in KEY_NAMES:
            if not self.hands_info[key]['empty']:
                categories_and_hands = list(self.hands_info[key]['categories']) + self.hands_info[key]['hands']
                categories_and_hands_str = ' OR '.join(categories_and_hands)
                output_str += (f"Player {self.player_num} {self.preflop} {self.pattern} "
                               f"board${self.filename}  AND ({categories_and_hands_str}) {key}\n\n")


        return output_str


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
        all_values = board.values + hand.values

        if 2 in all_values and 14 in all_values:
            ace_index = all_values.index(14)
            all_values[ace_index] = 1

        all_values.sort()

        straight = True
        for i in range(len(all_values) - 1):
            if all_values[i] + 1 != all_values[i + 1]:
                straight = False
                break

        return straight

    @staticmethod
    def is_HaveOverPair(board: Board, hand: Hand) -> bool:
        board_max_value = board.cards_info[0]['value']
        return board_max_value < hand.values[0] and board_max_value < hand.values[1]

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

    @staticmethod
    def is_flush12(board: Board, hand: Hand) -> bool:
        is_flush = Category.is_HaveFlush(board, hand)
        return is_flush and (hand.values[0] > 12)

    @staticmethod
    def is_flushBetween9and12(board: Board, hand: Hand) -> bool:
        is_flush = Category.is_HaveFlush(board, hand)
        return is_flush and (9 <= hand.values[0] <= 12)

    @staticmethod
    def is_flushUnder8(board: Board, hand: Hand) -> bool:
        is_flush = Category.is_HaveFlush(board, hand)
        return is_flush and (hand.values[0] <= 8)

    @staticmethod
    def is_HaveStraightFlush(board: Board, hand: Hand) -> bool:
        is_straight = Category.is_HaveStraight(board, hand)
        is_flush = Category.is_HaveFlush(board, hand)
        return is_straight and is_flush


# a list of dictionaries to store all the category functions and their corresponding string value to output
# this will make my life easier to loop through all the category checks 🙂
categories = [{'category_func': Category.is_HaveStraightFlush, 'str': 'HaveStraightFlush'},
              {'category_func': Category.is_HaveQuads, 'str': 'HaveQuads'},
              {'category_func': Category.is_HaveFullHouse, 'str': 'HaveFullHouse'},
              {'category_func': Category.is_flush12, 'str': 'f$flush_12'},
              {'category_func': Category.is_flushBetween9and12, 'str': 'f$flushbetwine9and12'},
              {'category_func': Category.is_flushUnder8, 'str': 'f$flushunder8'},

              {'category_func': Category.is_HaveStraight, 'str': 'HaveStraight'},
              {'category_func': Category.is_HaveTopSet, 'str': 'HaveTopSet'},
              {'category_func': Category.is_HaveSet, 'str': 'HaveSet'},
              {'category_func': Category.is_HaveTrips, 'str': 'HaveTrips'},

              {'category_func': Category.is_HaveTopTwoPair, 'str': 'HaveTopTwoPair'},
              {'category_func': Category.is_HaveTwoPair, 'str': 'HaveTwoPair'},
              {'category_func': Category.is_HaveBottomTwoPair, 'str': 'HaveBottomTwoPair'},

              {'category_func': Category.is_HaveTopPair, 'str': 'HaveTopPair'},
              {'category_func': Category.is_HaveSecondTopPair, 'str': 'HaveSecondTopPair'},
              {'category_func': Category.is_HaveThirdTopPair, 'str': 'HaveBottomPair'},
              {'category_func': Category.is_HaveOverPair, 'str': 'HaveOverPair'},
              ]

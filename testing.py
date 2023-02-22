from utils import Board, Hand, Category

# Information about how to use this file
# -------------------------------------------
# These are some sample test cases that I wrote, feel free to change them and new ones
# each dict has a board and func property that you can use to apply func on board

# each value of list of expected corresponds to each value of list of hands
# therefore make sure the ordering of hands and expected match
# for example if you want the first hands value to return True then put True in the first value of expected

cases = [
         {'board': 'Ac5d2c', 'hands': ['As6d', '5s6d'], 'expected':[True, False], 'func': Category.is_HaveTopPair},
         {'board': 'Ac5d2c', 'hands': ['5s6d'], 'expected':[True], 'func': Category.is_HaveSecondTopPair},
         {'board': 'Ac5d2c', 'hands': ['2s6d'], 'expected':[True], 'func': Category.is_HaveThirdTopPair},

         {'board': 'AsKd2c', 'hands': ['KdAs'], 'expected':[True], 'func': Category.is_HaveTopTwoPair},
         {'board': 'KsAd2c', 'hands': ['Ks2d'], 'expected':[True], 'func': Category.is_HaveBottomTwoPair},
         {'board': 'KcAd2c', 'hands': ['As2d'], 'expected':[True], 'func': Category.is_HaveTwoPair},

         {'board': 'Ks2dAc', 'hands': ['AdAc'], 'expected':[True, True], 'func': Category.is_HaveTopSet},
         {'board': 'AsKd2c', 'hands': ['2s2d', 'KsKc'], 'expected':[True, True], 'func': Category.is_HaveSet},

         {'board': 'AsAd2c', 'hands': ['As6d'], 'expected':[True], 'func': Category.is_HaveTrips},
         {'board': 'As2dAc', 'hands': ['AcAh'], 'expected':[True], 'func': Category.is_HaveQuads},
         {'board': 'AsAdAc', 'hands': ['Ac7h'], 'expected':[True], 'func': Category.is_HaveQuads},
         {'board': 'Ac5c2c', 'hands': ['Kc7c'], 'expected':[True], 'func': Category.is_HaveFlush},

         {'board': '5s4d2h', 'hands': ['3dAs'], 'expected':[True], 'func': Category.is_HaveStraight},
         {'board': 'Jd9sQh', 'hands': ['8hTc'], 'expected':[True], 'func': Category.is_HaveStraight},
         {'board': 'TsAhKd', 'hands': ['JhQd'], 'expected':[True], 'func': Category.is_HaveStraight},

         {'board': 'AcKd8c', 'hands': ['6s7d', '2c5d'], 'expected':[True, True], 'func': Category.is_HaveOverPair},
         {'board': '5c5d2c', 'hands': ['2s2d', '5h2d'], 'expected':[True, True], 'func': Category.is_HaveFullHouse}

         ]


# DO NOT CHANGE CODE BELOW THIS LINE
# --------------------------------------------------


passed_all = True

for case in cases:
    board = Board(case['board'])

    for hand_str, expected in zip(case['hands'], case['expected']):
        hand = Hand(hand_str)
        result = case['func'](board, hand)
        if result != expected:
            passed_all = False
            print(f'Failed case for board:{case["board"]}  hand: {hand_str}')
            print(f'function: {case["func"].__name__} result: {result} expected: {expected}')
            print()


if passed_all:
    print('Passed all cases...')
else:
    print("Couldn't pass all cases...")

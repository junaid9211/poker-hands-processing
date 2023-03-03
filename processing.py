import re
from variables import patterns, COLUMN_NAMES
from utils import Board, Hand, Category


# a list of dictionaries to store all the category functions and their corresponding string value to output
# this will make my life easier to loop through and perform all the category checks 🙂
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



def get_data_lines(file_path: str) -> list:
    # read the data and return list of lines
    with open(file_path, mode='r') as f:
        data_lines = f.read().splitlines()

    return data_lines


def save_output(file_path: str, output_list: list) -> None:
    with open(file_path, mode='w') as f:
        for output in output_list:
            output_str = output.get_output()
            f.write(output_str)

def get_filename(data_lines):
    for line in data_lines:
        m = re.search('File Name: (\w+)', line)
        if m:
            return m.group(1)


def get_rstring(line):
    """if the line contains a rstring then it will return the r string"""
    found = re.search('r\:0[\:\w]*', line)
    if found:
        rstring = found.group()
        if rstring[-1] != 'f':
            return rstring


def get_pattern(rstring):
    """gets a rstring and returns pattern of c and b"""
    pattern = ''
    for c in rstring:
        if c in ['c', 'b']:
            pattern += c

    return patterns[pattern]


def is_hand_line(line):
    return bool(re.search(r'^\w{4}:', line))


def get_hand_str_column_nums(hand_line):
    line = hand_line.split(':')
    hand_str = line[0]
    column_nums = ''.join(re.findall(r'\d', line[1]))

    return hand_str, column_nums


def get_key(column_nums: str):
    key_name = ''

    # if there are 3 columns
    if len(column_nums) == 3:
        if column_nums[0] == '1':
            key_name = COLUMN_NAMES[2]  # Raise
        elif column_nums[1] == '1':
            key_name = COLUMN_NAMES[3]  # Call
        else:
            key_name = COLUMN_NAMES[4]  # Fold
    else:
        if column_nums[0] == '1':
            key_name = COLUMN_NAMES[0]  # Bet
        else:
            key_name = COLUMN_NAMES[1]  # Check

    return key_name



def get_category(board: Board, hand: Hand):
    for category in categories:
        category_func = category['category_func']
        category_str = category['str']
        if category_func(board, hand):
            # if category is found then return its corresponding string value
            return category_str

    # if there is no category then return None
    return None
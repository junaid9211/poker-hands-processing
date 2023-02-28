import re
from variables import patterns
from collections import defaultdict
import os
from utils import Board, Hand, categories

def get_data_lines(file_path: str) -> list:
    # read the data and return list of lines
    with open(file_path, mode='r') as f:
        data_lines = f.read().splitlines()

    return data_lines


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
            key_name = 'Raise'
        elif column_nums[1] == '1':
            key_name = 'Call'
        else:
            key_name = 'Fold'
    else:
        if column_nums[0] == '1':
            key_name = 'Bet'
        else:
            key_name = 'Check'

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
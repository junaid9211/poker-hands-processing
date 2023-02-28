from collections import defaultdict
import re
from utils import Board, Hand, Output
from processing import (get_data_lines, get_filename,
                        get_key, get_rstring, get_hand_str_column_nums,
                        get_pattern, is_hand_line, get_category)



def switch_player():
    global player_num

    # if player_num == 0:
    #     player_num = 1

    if player_num == 1:
        player_num = 2

    elif player_num == 2:
        player_num = 1



player_num = 1
preflop = 'preflop'
rstring = ''

# TODO 1: [x]  Open the file and get list of lines
PATH = 'inputs/example-1.txt'
input_data_lines = get_data_lines(PATH)
output_list = []
file_name = get_filename(input_data_lines)
board = Board(file_name)

# TODO 2: [x] create hands_info dict to keep track of all hands and categories
KEY_NAMES = ['Bet', 'Check', 'Raise', 'Call', 'Fold']
hands_info = {
    key: {'hands': [], 'categories': set(), 'empty': True} for key in KEY_NAMES
}

# TODO 3: [x] loop through all lines of input data
for i in range(len(input_data_lines)):

    # TODO 4: [x] get rstring or hand_str
    if get_rstring(input_data_lines[i]):
        rstring = get_rstring(input_data_lines[i])

    elif is_hand_line(input_data_lines[i]):
        hand_str, column_nums = get_hand_str_column_nums(input_data_lines[i])

        hand = Hand(hand_str)
        column_name = get_key(column_nums)
        hands_info[column_name]['empty'] = False

        # TODO 5: [x] extract information and put it in hands_info dict
        category = get_category(board, hand)
        if category:
            hands_info[column_name]['categories'].add(category)
        else:
            hands_info[column_name]['hands'].append('hand$' + hand_str)


    # TODO 5: need to output data
    if i + 1 < len(input_data_lines):

        # if next line is rstring
        if get_rstring(input_data_lines[i + 1]):
            # create an output object ?
            # what if there was nothing above?
            contains_output = False
            for key in KEY_NAMES:
                if not hands_info[key]['empty']:
                    contains_output = True

            if contains_output:
                output = Output(player_num, preflop, get_pattern(rstring), file_name, hands_info)
                output_list.append(output)
                switch_player()


            hands_info = {
                key: {'hands': [], 'categories': set(), 'empty': True} for key in KEY_NAMES
            }



# TODO 6: now I need to save the output in a file
with open('output.txt', mode='w') as f:
    for output in output_list:
        output_str = output.get_output()
        f.write(output_str

                )
from utils import Board, Hand, Output
from variables import preflop, COLUMN_NAMES
from processing import (get_data_lines, save_output, get_filename,
                        get_key, get_rstring, get_hand_str_column_nums,
                        get_pattern, is_hand_line, get_category)





# TODO 1: [x]  Open the file and get list of lines
INPUT_PATH = 'other inputs/2s2h2d.cfr.txt'
OUTPUT_PATH = 'outputs'

player_num = 1
rstring = ''

input_data_lines = get_data_lines(INPUT_PATH)
output_list = []
file_name = get_filename(input_data_lines)
board = Board(file_name)

# TODO 2: [x] create hands_info dict to keep track of all hands and categories

hands_info = {
    key: {'hands': [], 'categories': set(), 'empty': True} for key in COLUMN_NAMES
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


    # TODO 6: [x] need to output data
    if i + 1 < len(input_data_lines):

        # if next line is rstring
        if get_rstring(input_data_lines[i + 1]):
            # check if there was some content after rstring line
            contains_output = False
            for key in COLUMN_NAMES:
                if not hands_info[key]['empty']:
                    contains_output = True

            # TODO 7: [x] create an output object and append it in the list of outputs
            if contains_output:
                output = Output(player_num, preflop, get_pattern(rstring), file_name, hands_info)
                output_list.append(output)

                # switch player
                if player_num == 1:
                    player_num = 2

                elif player_num == 2:
                    player_num = 1

            hands_info = {
                key: {'hands': [], 'categories': set(), 'empty': True} for key in COLUMN_NAMES
            }


# TODO 8: [x] now finally I need to save the output in a file
save_output('output2.txt', output_list)
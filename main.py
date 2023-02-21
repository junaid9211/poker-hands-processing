import re
from variables import patterns
from collections import defaultdict
import os

preflop = 'pre'

def get_filename(data):
    for line in data.split('\n'):
        m = re.search('File Name: (\w+)', line)
        if m:
            return m.group(1)


def get_rstring(line):
    found = re.search('r\:0[\:\w]*', line)
    if found:
        rstring = found.group()
        if rstring[-1]!='f':
            return rstring

        
def get_pattern(rstring):
    pattern = ''
    for c in rstring:
        if c in ['c', 'b']:
            pattern += c
    return pattern
  
    
def is_hands_string(s):
    return bool(re.search('^\w{4}:', s))



def switch_player():
    global player_num
    print('called switch player', end='')
    
    if player_num==0:
        player_num=1
        
    elif player_num==1:
        player_num=2
        
    elif player_num==2:
        player_num=1
        

   
def get_key(nums):
    key_name = ''
    if len(nums)==3:
        if nums[0]=='1':
            key_name = 'Raise'
        elif nums[1]=='1':
            key_name = 'Call'
        else:
            key_name = 'Fold'
    else:
        if nums[0]=='1':
            key_name = 'Bet'
        else:
            key_name = 'Check'
            
    return key_name




input_files = os.listdir('inputs')
if not os.path.exists('outputs'):
    os.mkdir('outputs')
    
    
for input_file_name in input_files:
    rstring = ''
    
    player_num = 1
    hands = defaultdict(lambda : [])
    
    print(f'Processing: {input_file_name}', end='')
    output_file = open(f'outputs/{input_file_name}', mode='w')
                       
    with open(f'inputs/{input_file_name}', mode='r') as f:
        data = f.read()
    
    lines = data.split('\n')
    filename = get_filename(data)                   
                       
    for i  in range(len(lines)):
        
        if get_rstring(lines[i]):
            rstring = get_rstring(lines[i])

        elif is_hands_string(lines[i]):       
            try:
                line = lines[i].split(':')
                chars = line[0]
                nums = ''.join(re.findall(r'\d', line[1]))

                hands[get_key(nums)].append(chars)
            except:
                print('error')


        if i+1 < len(lines):

            if get_rstring(lines[i+1]):
                writing = False
                keys = ['Bet', 'Check', 'Raise', 'Call', 'Fold']

                for key in keys:
                    if len(hands[key])>0:
                        # print(f"Player {player_num} {preflop} {patterns[get_pattern(rstring)]} board${filename} ({' OR '.join(hands[key])}) {key}\n\n") 
                        
                        for i in range(len(hands[key])):
                            hands[key][i] = 'hand$'+hands[key][i]

                        output_file.write(f"Player {player_num} {preflop} {patterns[get_pattern(rstring)]} board${filename}  AND ({' OR '.join(hands[key])}) {key}\n\n") 
                        writing = True



                hands = defaultdict(lambda : [])
                print(f'{rstring}:player {player_num}', end='| ')
                if writing:
                    switch_player()
                print(f'player {player_num}')

                
    print('Done ...')
    output_file.close()
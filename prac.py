keys = ['Bet', 'Check', 'Raise', 'Call', 'Fold']
hands_info = {
    key: {'hands': [], 'categories': set(), 'empty': True} for key in keys
}

print(hands_info)
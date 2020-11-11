def get_value_from_choices(choices, key):
    for choice in choices:
        if choice[0] == key:
            return choice[1]
    return None

import os


def get_value_from_choices(choices, key):
    for choice in choices:
        if choice[0] == key:
            return choice[1]
    return None


def delete_file(document):
    path = os.path.abspath(document.path)
    os.remove(path)
import collections
import json
import pathlib


DRINKS_PATH = pathlib.Path(__file__).parent / 'data/drinks.json'


def get_drinks(drinks_path=DRINKS_PATH):
    with drinks_path.open() as f:
        return collections.OrderedDict(sorted(json.load(f).items(), key=lambda i: i[1]['rank']))


DRINKS = get_drinks()

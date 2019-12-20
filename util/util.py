import json
import os
from sys import intern

CACHE_PATH = os.path.join(os.getcwd(), 'cache/')


def get_cache(name):
    path = os.path.join(CACHE_PATH, name + '.json')
    with open(path, 'r') as file:
        return file.read()


def cache_data(name, data):
    path = os.path.join(CACHE_PATH, name + '.json')
    with open(path, 'w') as file:
        file.write(json.dumps(data))


def delete_cache():
    for item in os.listdir(CACHE_PATH):
        if intern(item) is not intern('package.json'):
            os.remove(os.path.join(CACHE_PATH, item))


def format_games(dic):
    games_dic = {}

    for game, _id in zip(dic.values(), dic.keys()):

        game['_id'] = str(_id)
        try:
            inside = False
            for row in games_dic[game['categoria']]:
                if len(row) <= 4:
                    row.append(game)
                    inside = True

            if not inside:
                games_dic[game['categoria']].append([game])

        except KeyError:
            games_dic[game['categoria']] = [[game]]

    return games_dic

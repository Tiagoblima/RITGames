import json
import os
from sys import intern

import requests

from util.util import get_cache


def save_user(form):
    response = requests.post("https://rit-bd.herokuapp.com/conta/cadastrar/" +
                             form.first_name.data + ' ' + form.last_name.data + '/' +
                             form.username.data + '/' +
                             form.password.data + '/' +
                             form.email.data + '/' + 'user')

    print(response.status_code)

    if response.status_code is 200:
        return "Cadastro Realizado com sucesso!"
    else:
        return "Erro ao cadastrar tente novamente"


def do_login(username='', password=''):
    user = ''
    try:
        user = get_cache(username)
    except FileNotFoundError:
        response = requests.get("https://rit-bd.herokuapp.com/conta/logar/" + username + '/' + password)

        if response.status_code is 200:
            user = response.content
    try:
        return True, json.loads(user)
    except json.decoder.JSONDecodeError:
        pass

    return False, "Login ou senha incorretos"


def add_game(game):
    print(game)
    response = requests.post('https://rit-gameserver.herokuapp.com/games/add/', json=game)
    return json.loads(response.content)["msg"]


def get_games_by_author(author):

    response = requests.get('https://rit-gameserver.herokuapp.com/games/' + author)
    print(response.content)
    try:

        return json.loads(response.content)
    except json.decoder.JSONDecodeError:
        return {"msg": "Erro ao carregar Dashboard"}

def get_games():
    response = requests.get('https://rit-gameserver.herokuapp.com/games/')
    print(response.content)
    return json.loads(response.content)


def get_game(_id):
    response = requests.get('https://rit-gameserver.herokuapp.com/games/' + _id)
    return response


def get_user(name):
    response = requests.get('https://rit-bd.herokuapp.com/conta/get-nome/' + name.replace(' ', '%20'))
    print(response.status_code)
    print(response.content)
    if response.status_code is 200:
        return json.loads(response.content)

    return {'msg': "Homepage unreachable"}

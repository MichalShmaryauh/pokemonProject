from flask import Flask, Response, request
from poke_api_requests import *
from db_access import *
import json

app = Flask(__name__)


@app.route('/')
def home_page():
    return Response("WELCOME TO POKEMON GAME")


@app.route('/update_type/<name>', methods=['PUT'])
def update_type(name):
    try:
        pokemon_data = get_pokemon_info(name)
        res = update_types(pokemon_data)
        return Response(json.dumps(res["message"]), res["status"])
    except ConnectionError as errc:
        return Response("Connection error: {}".format(errc.args), 503)
    except requests.exceptions.HTTPError as errh:
        return Response("Http Error: {}".format(errh.args), errh.response.status_code)
    except requests.exceptions.Timeout as errt:
        print("Timeout Error: {}".format(errt.args), 408)
    except requests.exceptions.RequestException as err:
        print("OOps: Something Else", 400)


@app.route('/add/<name>', methods=['POST'])
def create_pokemon(name):
    res = get_pokemon_info(name)
    pokemon = {k: res.json()[k] for k in ["id", "name", "height", "weight"]}
    ret_val = add_pokemon(pokemon)
    if ret_val["status"] != 200:
        return Response(ret_val["message"], ret_val["status"])
    return Response(json.dumps(pokemon), 201)


@app.route('/get_pokemons/<type>', methods=['GET'])
def get_pokemon_type(type):
    res = get_pokemon_by_type(type)
    if res["status"] == 200:
        return Response(json.dumps(res["message"]), res["status"])
    return Response(json.dumps(res["message"]), res["status"])


@app.route('/get_trainer_pokemons/<trainer_name>', methods=['GET'])
def get_pokemon_trainer(trainer_name):
    res = get_pokemon_by_trainer(trainer_name)
    if res["status"] == 200:
        return Response(json.dumps(res["message"]), res["status"])
    return Response(json.dumps(res["message"]), res["status"])


@app.route('/get_trainers/<pokemon_name>', methods=['GET'])
def get_trainer_pokemon(pokemon_name):
    res = get_trainer_by_pokemon(pokemon_name)
    if res["status"] == 200:
        return Response(json.dumps(res["message"]), res["status"])
    return Response(res["message"], res["status"])


@app.route('/delete', methods=['DELETE'])
def delete_pokemon():
    pokemon_name = request.get_json().get("pokemon_name")
    trainer_name = request.get_json().get("trainer_name")
    res = delete_pokemon_of_trainer(pokemon_name, trainer_name)
    if res["status"] == 200:
        return Response(json.dumps(res["message"]), res["status"])
    return Response(res["message"], res["status"])


@app.route('/chain_next_pokemon', methods=['PUT'])
def get_chain_next_pokemon_post():
    pokemon_name = request.get_json().get("pokemon_name")
    trainer_name = request.get_json().get("trainer_name")

    if not check_pair_exist(pokemon_name, trainer_name):
        return Response("{} does not have a {} pokemon".format(trainer_name, pokemon_name), 400)
    info = get_evolution_chain_info(pokemon_name)
    evolves_to = info.json()["chain"]["evolves_to"]
    next_pokemon = info.json()["chain"]["species"]["name"]
    if len(evolves_to) > 0:
        p_info = get_pokemon_info(next_pokemon)
        delete_pokemon_trainer(pokemon_name, trainer_name)
        update_pokemon(p_info.json(), trainer_name)
        return Response(json.dumps(next_pokemon), 200)
    else:
        return Response("{} can not evolve".format(pokemon_name), 400)

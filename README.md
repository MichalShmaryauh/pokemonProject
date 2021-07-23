### Pokemon Project
Server requests:
* Update pokemon types-\
url: 'http://127.0.0.1:3000/update_type/<pokemon_name>' \
method:PUT\
response: list of pokemon types if succeeded else error message

* Add pokemon-\
url: 'http://127.0.0.1:3000/add/<pokemon_name>' \
method:POST\
response: pokemon data if succeeded else error message

* Get pokemons by type-\
url: 'http://127.0.0.1:3000/get_pokemons/<pokemon_type>' \
method:GET\
response: list of pokemons' names has type if succeeded else error message

* Get pokemons by trainer-\
url: 'http://127.0.0.1:3000/get_trainer_pokemons/<trainer_name>' \
method:GET\
response: list of pokemons' names has trainer if succeeded else error message

* Get trainers of a pokemon\
url: 'http://127.0.0.1:3000/get_trainers/<pokemon_name>' \
method:GET\
response: list of trainers of pokemon has pokemon_name if succeeded else error message

* Evolve \
url: 'http://127.0.0.1:3000/chain_next_pokemon' \
method:PUT\
params:pokemon_name,trainer_name\
response: name of the evolved pokemon if succeeded else error message

* Delete pokemon of trainer\
url: 'http://127.0.0.1:3000/delete' \
method:DELETE\
params:pokemon_name,trainer_name\
response: "Deleted successfully!" if succeeded else error message

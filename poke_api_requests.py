import requests
from config import pokeapi_url


def get_pokemon_info(pokemon_name):
    return requests.get(url='{}{}'.format(pokeapi_url, pokemon_name),
                        headers={'User-agent': 'your bot 0.1'},
                        verify=False)


def get_species_url(pokemon_name):
    res = requests.get(url='{}{}'.format(pokeapi_url, pokemon_name),
                       headers={'User-agent': 'your bot 0.1'},
                       verify=False)
    species_url = res.json()["species"]["url"]
    return species_url


def get_chain(pokemon_name):
    evolution_chain_url = get_evolution_chain_url(pokemon_name)
    res = requests.get(url='{}'.format(evolution_chain_url),
                       headers={'User-agent': 'your bot 0.1'},
                       verify=False)
    chain = res.json()["chain"]
    return chain


def get_species_info(pokemon_name):
    species_url = get_species_url(pokemon_name)
    res = requests.get(url='{}'.format(species_url),
                       headers={'User-agent': 'your bot 0.1'},
                       verify=False)
    return res.json()


def get_evolution_chain_url(pokemon_name):
    species_url = get_species_url(pokemon_name)
    res = requests.get(url='{}'.format(species_url),
                       headers={'User-agent': 'your bot 0.1'},
                       verify=False)

    evolution_chain_url = res.json()["evolution_chain"]["url"]
    return evolution_chain_url


def get_evolution_chain_info(pokemon_name):
    evolution_chain_url = get_evolution_chain_url(pokemon_name)
    res = requests.get(url='{}'.format(evolution_chain_url),
                       headers={'User-agent': 'your bot 0.1'},
                       verify=False)
    return res.json()

import unittest
import requests, json

from server import *


class MyTestCase(unittest.TestCase):
    def test_get_pokemon_by_type(self):
        res = requests.get(url='http://127.0.0.1:3000/get_pokemons/normal',
                           headers={'User-agent': 'your bot 0.1'},
                           verify=False)
        self.assertIn('eevee', res.json()[19])

    def test_add_pokemon(self):
        create_pokemon("yanma")
        bug_res = requests.get(url='http://127.0.0.1:3000/get_pokemons/bug',
                               headers={'User-agent': 'your bot 0.1'},
                               verify=False)
        flying_res = requests.get(url='http://127.0.0.1:3000/get_pokemons/flying',
                                  headers={'User-agent': 'your bot 0.1'},
                                  verify=False)
        self.assertEqual('yanma', flying_res.text.replace('[', '').replace(']', '').replace('"', ''))
        self.assertEqual('yanma', bug_res.json()[12])

    def test_update_pokemon_types(self):
        type_res = requests.put(url='http://127.0.0.1:3000/update_type/venusaur',
                                headers={'User-agent': 'your bot 0.1'},
                                verify=False)
        for t in type_res.json():
            res = requests.get(url='http://127.0.0.1:3000/get_pokemons/{}'.format(t),
                               headers={'User-agent': 'your bot 0.1'},
                               verify=False)
            self.assertTrue('venusaur' in res.json())

    def test_get_pokemons_by_owner(self):
        pokemons = ["wartortle", "caterpie", "beedrill", "arbok", "clefairy", "wigglytuff", "persian", "growlithe",
                    "machamp", "golem", "dodrio", "hypno", "cubone", "eevee", "kabutops"]
        res = requests.get(url='http://127.0.0.1:3000/get_trainer_pokemons/Drasna')
        self.assertEqual(pokemons, res.json())

    def test_get_owners_of_a_pokemon(self):
        trainers = ['Whitney', 'Giovanni', 'Jasmine']
        res = requests.get(url='http://127.0.0.1:3000/get_trainers/charmander',
                           headers={'User-agent': 'your bot 0.1'},
                           verify=False)
        self.assertEqual(trainers, res.json())

    def test_evolve(self):
        res = requests.put(url="http://127.0.0.1:3000/chain_next_pokemon",
                           json={"pokemon_name": "spearow", "trainer_name": "Archie"})
        self.assertEqual(res.text, "Archie does not have a spearow pokemon")


if __name__ == '__main__':
    unittest.main()

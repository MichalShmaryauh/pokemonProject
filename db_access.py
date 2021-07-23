import pymysql
from config import connection_config

connection = pymysql.connect(
    host=connection_config["host"],
    user=connection_config["user"],
    password=connection_config["password"],
    db=connection_config["db"],
    charset="utf8",
    cursorclass=pymysql.cursors.DictCursor
)


def update_types(pokemon_data):
    types = pokemon_data.json().get("types")
    if connection.open:
        with connection.cursor() as cursor:
            try:
                for type in types:
                    query = "SELECT * FROM POKEMONTYPES WHERE POKEMON_ID={} AND TYPE='{}'".format(
                        pokemon_data.json()["id"],
                        type["type"]["name"])

                    cursor.execute(query)
                    select_res = cursor.fetchall()
                    if len(select_res):
                        continue
                    query = "INSERT INTO POKEMONTYPES(POKEMON_ID,TYPE) VALUES({},'{}');".format(
                        pokemon_data.json().get("id"),
                        type["type"]["name"])
                    cursor.execute(query)
                connection.commit()
                return {"message": [t["type"]["name"] for t in types], "status": 200}
            except pymysql.err.ProgrammingError as err:
                return {"message": "Executing query failed.\n{}".format(err), "status": 500}
    else:
        return {"message": "Accessing DB failed.", "status": 500}


def add_pokemon(pokemon):
    if connection.open:
        try:
            with connection.cursor() as cursor:
                query = "SELECT * FROM POKEMON WHERE NAME='{}';".format(pokemon["name"])
                cursor.execute(query)
                res = cursor.fetchall()
                if not len(res):
                    query = "INSERT INTO POKEMON(ID,NAME,HEIGHT,WEIGHT) VALUES ({},'{}',{},{});" \
                        .format(pokemon["id"],
                                pokemon["name"],
                                pokemon["height"],
                                pokemon["weight"])
                    cursor.execute(query)
                    connection.commit()
                    return {'message': "successful", "status": 200}
                return {'message': 'already exist', 'status': 400}
        except pymysql.err.ProgrammingError as err:
            return {"message": "Executing query failed.\n{}".format(err), "status": 500}
    else:
        return {"message": "Accessing DB failed.", "status": 500}


def get_pokemon_by_type(type):
    if connection.open:
        with connection.cursor() as cursor:
            query = "SELECT NAME FROM POKEMON JOIN POKEMONTYPES ON POKEMON.ID=POKEMONTYPES.POKEMON_ID" \
                    " WHERE POKEMONTYPES.TYPE='{}';".format(type)
            try:
                cursor.execute(query)
                res = cursor.fetchall()
            except pymysql.err.ProgrammingError as err:
                return {"message": "Executing query failed.\n{}".format(err.args), "status": 500}
        connection.commit()
        return {"message": [p["NAME"] for p in res], "status": 200}
    else:
        return {"message": "Accessing DB failed.", "status": 500}


def get_pokemon_by_trainer(trainer_name):
    if connection.open:
        with connection.cursor() as cursor:
            query = "SELECT Pokemon.name From Pokemon JOIN OwnedBy Join Trainer ON Pokemon.id =OwnedBy.pokemon_id " \
                    "and Trainer.id =OwnedBy.trainer_id WHERE Trainer.name='{}';".format(
                trainer_name)
            try:
                cursor.execute(query)
                result = cursor.fetchall()
                connection.commit()
                return {"message": [p["name"] for p in result], "status": 200}
            except pymysql.err.ProgrammingError as err:
                return {"message": "Executing query failed.\n{}".format(err), "status": 500}
    else:
        return {"message": "Accessing DB failed.", "status": 500}


def get_trainer_by_pokemon(pokemon_name):
    if connection.open:

        with connection.cursor() as cursor:
            query = "SELECT Trainer.name From  Pokemon JOIN  OwnedBy Join Trainer ON Pokemon.id " \
                    "=OwnedBy.pokemon_id and Trainer.id =OwnedBy.trainer_id WHERE Pokemon.name='{}';".format(
                pokemon_name)
            try:
                cursor.execute(query)
                result = cursor.fetchall()
                connection.commit()
                return {"message": [t["name"] for t in result], "status": 200}
            except pymysql.err.ProgrammingError as err:
                return {"message": "Executing query failed.\n{}".format(err), "status": 500}
    else:
        return {"message": "Accessing DB failed.", "status": 500}


def delete_pokemon_of_trainer(pokemon_name, trainer_name):
    if connection.open:
        with connection.cursor() as cursor:
            try:
                query = "DELETE FROM OWNEDBY WHERE POKEMON_ID=(SELECT ID FROM POKEMON WHERE NAME='{}') AND" \
                        " TRAINER_ID=(SELECT ID FROM TRAINER WHERE NAME='{}');".format(pokemon_name, trainer_name)
                cursor.execute(query)
                connection.commit()
                return {"message": "Deleted successfully!", "status": 200}
            except pymysql.err.ProgrammingError as err:
                return {"message": "Executing query failed.\n{}".format(err), "status": 500}
    else:
        return {"message": "Accessing DB failed.", "status": 500}


def check_pair_exist(pokemon_name, trainer_name):
    query = "SELECT * FROM OWNEDBY WHERE POKEMON_ID=(SELECT ID FROM POKEMON WHERE NAME='{}') AND TRAINER_ID=(SELECT ID FROM TRAINER" \
            " WHERE NAME='{}');".format(pokemon_name, trainer_name)
    with connection.cursor() as cursor:
        cursor.execute(query)
        res = cursor.fetchall()
    return len(res)


def delete_pokemon_trainer(pokemon_name, trainer_name):
    if connection.open:
        with connection.cursor() as cursor:
            try:
                query = "DELETE FROM OWNEDBY WHERE POKEMON_ID=(SELECT ID FROM POKEMON WHERE NAME='{}') AND" \
                        " TRAINER_ID=(SELECT ID FROM TRAINER WHERE NAME='{}');".format(pokemon_name, trainer_name)
                cursor.execute(query)
                connection.commit()
                print("Deleted successfully!")
            except pymysql.err.ProgrammingError as err:
                print("Executing query failed.\n{}".format(err))
    else:
        print("Accessing DB failed.")


def update_pokemon(pokemon_info, trainer_name):
    if connection.open:
        try:
            with connection.cursor() as cursor:
                find_trainer_id = "SELECT ID FROM TRAINER WHERE NAME='{}';".format(trainer_name)
                cursor.execute(find_trainer_id)
                t_id = cursor.fetchall()[0].get("ID")
                query = "INSERT INTO OWNEDBY(POKEMON_ID,TRAINER_ID) VALUES ({},{});" \
                    .format(pokemon_info.get("id"), t_id)
                cursor.execute(query)
                find_pokemon = "SELECT * FROM POKEMON WHERE NAME='{}';".format(pokemon_info["name"])
                cursor.execute(find_pokemon)
                pokemon = cursor.fetchall()
                if not len(pokemon):
                    cursor.execute("INSERT INTO POKEMON(ID,NAME,HEIGHT,WEIGHT) VALUES({},'{}',{},{});".format(
                        pokemon_info["id"], pokemon_info["name"], pokemon_info["height"], pokemon_info["weight"]))
                    for pokemon_type in pokemon["types"]:
                        query_types = "INSERT INTO POKEMONTYPES(POKEMON_ID,TYPE) VALUES({},'{}');" \
                            .format(pokemon["id"], pokemon_type)
                        cursor.execute(query_types)
                connection.commit()
        except pymysql.err.ProgrammingError as err:
            return "Executing query failed.\n{}".format(err)
    else:
        return "Accessing DB failed."
    return pokemon

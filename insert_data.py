import pymysql, json

connection = pymysql.connect(host="localhost",
                             user="root",
                             password="211660022",
                             db="DB_pokemon",
                             charset="utf8",
                             cursorclass=pymysql.cursors.DictCursor)


def insert_data():
    with open('pokemon_data.json') as file:
        data = json.load(file)
        trainers = dict()
        pokemon_list = list()
        t_id = 0
        if connection.open:
            with connection.cursor() as cursor:
                for p in data:
                    query = "INSERT INTO POKEMON(ID,NAME,HEIGHT,WEIGHT) VALUES ('{}','{}',{},{});".format(
                        p["id"],
                        p["name"],
                        p["height"],
                        p["weight"])
                    cursor.execute(query)
                    query = "INSERT INTO POKEMONTYPES(POKEMON_ID,TYPE) VALUES({},'{}');".format(p["id"], p["type"])
                    cursor.execute(query)
                    for t in p["ownedBy"]:
                        if trainers.get("{}-{}".format(t["name"], t["town"])) is None:
                            trainers["{}-{}".format(t["name"], t["town"])] = t_id
                            query = "INSERT INTO TRAINER(ID,NAME,TOWN) VALUES ({},'{}','{}');".format(t_id, t["name"],
                                                                                                      t["town"])
                            cursor.execute(query)
                            t_id += 1
                        query = "INSERT INTO OWNEDBY(POKEMON_ID,TRAINER_ID) VALUES({},{});".format(p["id"], trainers[
                            '{}-{}'.format(t["name"], t["town"])])
                        cursor.execute(query)
    connection.commit()


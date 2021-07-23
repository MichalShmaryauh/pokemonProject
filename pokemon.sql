
use DB_Pokemon;

CREATE TABLE Pokemon(
     id INTEGER,
     name  VARCHAR(20),
     height INTEGER,
     weight INTEGER,
     PRIMARY KEY (id) 
);     


CREATE TABLE Trainer(
     id INTEGER,
    name  VARCHAR(20),
    town VARCHAR(20),
    PRIMARY KEY (id),
    UNIQUE (name,town)
); 
   
CREATE TABLE OwnedBy(
     id INTEGER AUTO_INCREMENT,
     pokemon_id  INTEGER,
     trainer_id INTEGER,
     PRIMARY KEY (id),  
     FOREIGN KEY(pokemon_id) REFERENCES Pokemon(id),
     FOREIGN KEY(trainer_id) REFERENCES Trainer(id)
);

CREATE TABLE PokemonTypes(
    pokemon_id  INTEGER,
    type VARCHAR(20),
    PRIMARY KEY (pokemon_id,type),  
    FOREIGN KEY(pokemon_id) REFERENCES Pokemon(id)
)








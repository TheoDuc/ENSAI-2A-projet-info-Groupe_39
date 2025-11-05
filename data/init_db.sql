-----------------------------------------------------
-- Joueur
-----------------------------------------------------
DROP TABLE IF EXISTS joueur CASCADE ;
CREATE TABLE joueur(
    id_joueur    SERIAL PRIMARY KEY,
    pseudo       VARCHAR(30) UNIQUE,
    credit       INTEGER,
    pays         VARCHAR(50)
);

-----------------------------------------------------
-- Manche
-----------------------------------------------------
DROP TABLE IF EXISTS manche CASCADE ;
CREATE TABLE manche(
    id_manche    SERIAL PRIMARY KEY,
    carte1       VARCHAR(50),
    carte2       VARCHAR(50),
    carte3       VARCHAR(50),
    carte4       VARCHAR(50),
    carte5       VARCHAR(50)
);
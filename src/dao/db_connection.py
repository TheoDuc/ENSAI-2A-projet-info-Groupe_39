"""Module de connection à la base de données"""

import dotenv
import psycopg2
from psycopg2.extras import RealDictCursor

from utils.singleton import Singleton


class DBConnection(metaclass=Singleton):
    """
    Classe gérant la connexion à la base de données PostgreSQL.

    Attributs
    ----------
    __connection : psycopg2.extensions.connection
        Objet de connexion PostgreSQL (RealDictCursor par défaut).

    Propriétés
    ----------
    connection : psycopg2.extensions.connection
        Retourne la connexion active à la base de données, permettant
        d’exécuter des requêtes SQL au sein d’un bloc contextuel
    """

    def __init__(self):
        """Ouverture de la connexion"""
        dotenv.load_dotenv()

        self.connection = psycopg2.connect(
            host="postgresql-275401.user-id2833",
            port=5432,
            user="user-id2833",
            password="tw1031qej52i6rmu1t8e",
            database="defaultdb",
            cursor_factory=RealDictCursor,
        )

    @property
    def connection(self):
        return self.__connection

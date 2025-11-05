"""Implémentation de la classe JoueurDAO"""

import logging

from business_object.joueur import Joueur
from business_object.info_manche import InfoManche
from business_object.manche import Manche
from dao.db_connection import DBConnection
from utils.log_decorator import log
from utils.singleton import Singleton


class MancheDao(metaclass=Singleton):
    """Classe contenant les méthodes pour accéder aux Manche de la base de données"""

    @log
    def creer(self, manche) -> bool:
        """Creation d'une manche dans la base de données

        Parameters
        ----------
        manche : Manche

        Returns
        -------
        created : bool
            True si la création est un succès
            False sinon
        """

        res = None

        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "INSERT INTO manche(carte1, carte2, carte3, carte4, carte5) "
                        " VALUES (%(carte1)s, %(carte2)s, %(carte3)s, %(carte4)s, %(carte5)s)"
                        " RETURNING id_manche;                                                ",
                        {
                            "carte1": manche.board.cartes[0],
                            "carte2": manche.board.cartes[1],
                            "carte3": manche.board.cartes[2],
                            "carte4": manche.board.cartes[3],
                            "carte5": manche.board.cartes[4]
                        },
                    )
                    res = cursor.fetchone()
        except Exception as e:
            logging.info(e)

        created = False
        if res:
            created = True

        return created


manchedao = MancheDao()
joueur1 = Joueur(1, 'paul', 100, 'fr')
joueur2 = Joueur(1, 'paul2', 1002, 'fr2')
infomanche = InfoManche([joueur1, joueur2])
manche = Manche(infomanche, 5)
# manche.preflop()
manche.flop()
manche.turn()
manche.river()
print(manche.board.cartes[1])
print(manchedao.creer(manche))

